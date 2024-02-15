# Ensures the environment is setup right

import constant
import os
from pathlib import Path

def checkOrCreate35Up(folder_name: str):
    """ Check or create a folder for python version 3.5 and up
    
    :param folder_name: String name of the folder.
    """
    Path(folder_name).mkdir(parents = True, exists = True)

def checkOrCreate35Down(folder_name: str):
    """ Check or create a folder for python version below 3.5
    
    :param folder_name: String name of the folder.
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def checkOrCreate(folder_name: str):
    """ Check or create a folder with a name
    
    :param folder_name: String name of the folder.
    """
    # Todo do a version check and run the correct function.
    checkOrCreate35Down(folder_name)
  
def init():
    checkOrCreate(constant.FOLDER_RAW)
    checkOrCreate(constant.FOLDER_OUTPUT)
    checkOrCreate(constant.FOLDER_LOGS)
    