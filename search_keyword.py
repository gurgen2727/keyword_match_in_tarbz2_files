#/usr/bin/env python
import os
import tarfile
import logging
# logging creation
logging.basicConfig(level=logging.INFO)

def search_keyword(root_path, keywords=None):
    """
    @param root_path: root path of directory that contains tar.gz2 files or subdirectories
    @type root_path: String
    @param keywords: List of keywords
    @type keywords: List
    @return None if error, otherwise
    """
    if not keywords:
        logging.error("Keywords attribute is empty")
        return None
    if os.path.exists(root_path):
        for root_dir, dir_list, file_list in os.walk(root_path):
            for file_el in file_list:
                tar_path = os.path.join(root_dir, file_el)
                if tar_path.endswith('tar.bz2'):
                    tar = tarfile.open(tar_path, "r:bz2")
                    try:
                        for tar_info in tar:
                            extract_file = tar.extractfile(tar_info)
                            if extract_file:
                                file_path = os.path.join(tar_path, tar_info.name)
                                for num, line in enumerate(extract_file, start=1):
                                    for keyword in keywords:
                                        if keyword in line:
                                            logging.info('keyword:%s %s %s %s' % (keyword, file_path, num, line))
                            else:
                                pass
                                # not a file, but directory os something else
                            tar.members = []
                    except EOFError:
                        logging.error("Tar file is corrupted: %s" % tar_path)
                        return None
                    finally:
                        tar.close()
    else:
        logging.error("Directory doesn't exit: '%s'" % root_path)
        return None

if __name__ == '__main__':
    search_keyword('/home/egs/Desktop/robo-2', ['2132080000?',
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
                                                '3102400028?'])