# csv processor
import os
from typing import TextIO

import constant
import csv
import env_setup
import logger
from datetime import datetime

env_setup.init()


# get or create output file based on date
def get_output_file(output_folder_name: str, date: datetime):
    """ Get a file to append new data to. Creates a new file with the name if it doesn't exist.
    
    :param output_folder_name: String name of the folder to use for output.
    :param date: Date of the file to grab.
    :return: File to work with. Should be closed when done.
    """
    file_name = output_folder_name + '/' + date.strftime('%d-%m-%Y.csv')

    if not os.path.exists(file_name):
        csv_file = open(file_name, 'a')
        csv_file.write(constant.CSV_OUTPUT_HEADER + '\n')
        return csv_file
    else:
        return open(file_name, 'a')


# get all raw files
# determine file type (USAA, Cap1, NFCU)
# Process file based on type and append to output file

now = datetime.now()
with logger.Logger(constant.FOLDER_LOGS) as logFile:
    logFile.print("******* Starting CSV processing *******", "info")
    logFile.print("Log file opened", "info")
    with get_output_file(constant.FOLDER_OUTPUT, now) as outFile:
        logFile.print("Got output file", "info")
        outFile.write(now.strftime('%d-%m-%Y, %H-%M-%S') + "\n")
        logFile.print("Closing output file", "info")
    logFile.print("--- Closing Log File", "info")
