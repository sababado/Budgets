# Ensures the environment is setup right
import os
import sys
from pathlib import Path

from bank_file_compiler import constant


def check_or_create_35_up(folder_name: str):
    """ Check or create a folder for python version 3.5 and up
    
    :param folder_name: String name of the folder.
    """
    if not Path(folder_name).exists():
        Path(folder_name).mkdir(parents=True)


def check_or_create_35_down(folder_name: str):
    """ Check or create a folder for python version below 3.5
    
    :param folder_name: String name of the folder.
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def check_or_create(folder_name: str):
    """ Check or create a folder with a name
    
    :param folder_name: String name of the folder.
    """
    # Todo do a version check and run the correct function.
    if sys.version_info >= (3, 5, 0):
        check_or_create_35_up(folder_name)
    else:
        check_or_create_35_down(folder_name)


def init():
    check_or_create(constant.FOLDER_DATA)
    check_or_create(constant.FOLDER_RAW)
    check_or_create(constant.FOLDER_OUTPUT)
    check_or_create(constant.FOLDER_LOGS)
