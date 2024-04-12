"""
This file is supposed to find all the python files under a directory, and store those python files to a directory
Why not just record the path to the python files? Because later we might want to use a web crawler.
"""

import os
import fnmatch
import shutil


def find_and_open_py_files(root_dir, destination_directory):
    for foldername, subfolders, filenames in os.walk(root_dir):
        for filename in filenames:
            if fnmatch.fnmatch(filename, '*.py'):
                original_filepath = os.path.join(foldername, filename)
                # copy the file to destination_directory
                destination_filepath = os.path.join(destination_directory, filename)
                shutil.copy(original_filepath, destination_filepath)


# chinese_root_directory = '/Users/samyiin/Projects/MyMastersThesis/RetrieveDataProject/DownloadProjects/ChineseProjects'
#
# chinese_destination_directory = '/Users/samyiin/Projects/MyMastersThesis/RetrieveDataProject/PyFiles/ChineseProjectPyFile'
#
# find_and_open_py_files(chinese_root_directory, chinese_destination_directory)

english_root_directory = '/Users/samyiin/Projects/MyMastersThesis/RetrieveDataProject/DownloadProjects/EnglishProjects'

english_destination_directory = '/Users/samyiin/Projects/MyMastersThesis/RetrieveDataProject/PyFiles/EnglishProjectPyFile'

find_and_open_py_files(english_root_directory, english_destination_directory)