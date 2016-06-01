#!/usr/bin/env python
# List of keywords
KEYWORDS = ['2132080000?',
            '2132080001?',
            '2132080002?',
            '2132080003?',
            '2132080004?',
            '3105010000?',
            '3105010002?',
            '3105010003?',
            '3105010001?',
            '3105010004?',
            '3235021084?',
            '3235021085?',
            '3235021088?',
            '3235021091?',
            '3235021100?',
            '3102400004?',
            '3102400009?',
            '3102400022?',
            '3102400023?',
            '3102400028?',
            'aaaa']

# Standard imports
import os
import sys
import tarfile
import threading
from threading import Thread
import logging
# logging creation
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] (%(threadName)s) %(message)s')
# thread lock release mechanism
lock = threading.Lock()


def search_keyword_in_tar(tar_path, file_des, keywords):
    """
    Function searches all keywords in specified tar.bz2
    in separate thread and write the result in file by doing
    safe multi-threading
    @param tar_path: path of tar.bz2
    @param file_des: output file descriptor
    @param keywords: list of keywords
    """
    tar = tarfile.open(tar_path, "r:bz2")
    try:
        logging.info("Analyzing %s" % tar_path)
        for tar_info in tar:
            extract_file = tar.extractfile(tar_info)
            if extract_file:
                file_path = os.path.join(tar_path, tar_info.name)
                for num, line in enumerate(extract_file, start=1):
                    for keyword in keywords:
                        if keyword in line:
                            lock.acquire()  # thread blocks at this line
                            file_des.write("keyword:%s file_name:%s line_number:%s line_content:%s" % (keyword, file_path, num, line))
                            lock.release()  # release thread
            else:
                pass
                # not a file, but directory os something else
            tar.members = []
    except EOFError:
        logging.error("Tar file is corrupted: %s" % tar_path)
        return None
    finally:
        tar.close()


def search_keyword(root_path, out_file_path, keywords=None):
    """
    Function searches all keywords in all tar.bz2 located under root_path recursively
    @param root_path: root path of directory that contains tar.bz2 files or subdirectories
    @type root_path: String
    @param out_file_path: output file path
    @type out_file_path: String
    @param keywords: List of keywords
    @type keywords: List
    @return None if error
    """
    if not keywords:
        logging.error("Keywords attribute is empty")
        return None
    if os.path.exists(root_path):
        with open(out_file_path, 'w') as file_des:
            # list of threads
            threads = []
            for root_dir, dir_list, file_list in os.walk(root_path):
                for file_el in file_list:
                    tar_path = os.path.join(root_dir, file_el)
                    if tar_path.endswith('tar.bz2'):
                        thread = Thread(target=search_keyword_in_tar,
                                        args=(tar_path, file_des, keywords))
                        thread.start()
                        threads.append(thread)
            # Waiting all threads to finish
            _ = [thr_el.join() for thr_el in threads]
    else:
        logging.error("Directory doesn't exit: '%s'" % root_path)
        return None

if __name__ == '__main__':
    try:
        root_path = sys.argv[1]
        out_file_path = sys.argv[2]
    except:
        logging.info("Please specify directory path of tar.bz2 and output file path")
        sys.exit(1)
    search_keyword(root_path, out_file_path, KEYWORDS)