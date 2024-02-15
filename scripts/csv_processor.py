# csv processor

import constant
import env_setup
from datetime import datetime

env_setup.init()


# get or create output file based on date
def get_output_file(output_folder_name: str, date: datetime):
    """ Get a file to append new data to.
    
    :param output_folder_name: String name of the folder to use for output.
    :param date: Date of the file to grab.
    :return: File to work with. Should be closed when done.
    """
    file_name = output_folder_name + '/' + date.strftime('%d-%m-%Y.csv')
    return open(file_name, 'a')


# get all raw files
# determine file type (USAA, Cap1, NFCU)
# Process file based on type and append to output file

now = datetime.now()
with get_output_file(constant.FOLDER_OUTPUT, now) as outFile:
    print("Got file")
    outFile.write(now.strftime('%d-%m-%Y, %H-%M-%S') + "\n")
    print("done with file")
