# csv processor
import os
from typing import TextIO

import constant
import csv
import env_setup
from logger import Logger
from datetime import datetime

env_setup.init()


# get all raw files
# determine file type (USAA, Cap1, NFCU)
# Process file based on type and append to output file

# get or create output file based on date
def get_output_file(output_folder_name: str, date: datetime):
    """ Get a file to append new data to. Creates a new file with the name if it doesn't exist.

    :param output_folder_name: String name of the folder to use for output.
    :param date: Date of the file to grab.
    :return: File to work with. Should be closed when done.
    """
    with Logger(constant.FOLDER_LOGS) as log_file:
        file_name = output_folder_name + '/' + date.strftime('%d-%m-%Y.csv')

        log_file.print("#Output file name: " + file_name)
        if not os.path.exists(file_name):
            log_file.print("#File didn't exist, creating and initializing...")
            csv_file = open(file_name, 'a')
            csv_file.write(constant.CSV_OUTPUT_HEADER + '\n')
            return csv_file
        else:
            log_file.print("#File existed, opening...")
            return open(file_name, 'a')


def check_file_source(csv_header: [str], file_name: str, log_file: Logger):
    """ Checks which type of account this file is from.
    :param log_file: The logger to log to.
    :param file_name: File name.
    :param csv_header: Header string array.
    :return: constant._FILE_TYPES The type of file this is.
    """
    for header, values in constant.HEADERS.items():
        header_values = values.split(',')
        log_file.print("%% Checking header: " + header)
        found_header: str = header
        if header_values == csv_header:
            if header == constant.HEADER_TYPE_USAA:
                if file_name.lower().__contains__("savings"):
                    found_header = constant.FILE_TYPE_USAA_SAVING
                else:
                    found_header = constant.FILE_TYPE_USAA_CHECKING

            log_file.print("%% Found header: " + found_header)
            return found_header
    log_file.print("%% Could not find any matching header: " + str(csv_header))


def process_file_usaa(row: list[str], bank_type: str, output_file: TextIO, log_file: Logger):
    amount = float(row[4])
    debit_credit_val: str = ''
    if amount < 0:
        debit_credit_val = str(abs(amount)) + ","
    else:
        debit_credit_val = "," + str(amount)

    output_file.write("%s,%s,%s,%s,%s,,\n"
                      % (row[0], bank_type, row[2], row[3], debit_credit_val))


def process_file(file_name: str, output_file: TextIO, log_file: Logger):
    """ Analyzes a file, categorizes it and appends data to the output file

    :param file_name: File to analyze
    :param output_file: Output file to write to.
    :param log_file: The logger to log to
    """
    log_file.print("% Analyzing file: " + file_name)
    with open(file_name, 'r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        bank_type = ''
        # Determine bank type
        for row in csv_reader:
            if not row:
                continue
            # Find the bank type
            if bank_type == '':
                log_file.print("% No bank type yet... Checking: " + row.__str__())
                bank_type = check_file_source(row, file_name, log_file)
                log_file.print("% Found bank type: " + str(bank_type), "info")
            else:
                # Act on the bank type
                log_file.print("%-- Processing row: " + bank_type + ": " + str(row))
                # Capital One
                if bank_type == constant.FILE_TYPE_CAPITALONE:
                    output_file.write("%s,%s,%s,%s,%s,,\n"
                                      % (row[0], row[2], row[3], row[4], row[5]))

                # NFCU
                if bank_type == constant.FILE_TYPE_NFCU:
                    output_file.write("%s,%s,%s,,%s,%s,,\n"
                                      % (row[0], bank_type, row[2], row[3], row[4]))
                # USAA
                if bank_type == constant.FILE_TYPE_USAA_CHECKING or bank_type == constant.FILE_TYPE_USAA_SAVING:
                    process_file_usaa(row, bank_type, output_file, log_file)
                # Uh Oh
                else:
                    log_file.print("^&^&^&^&^^&No bank type found for this row")


now = datetime.now()
with Logger(constant.FOLDER_LOGS) as logFile:
    logFile.print("******* Starting CSV processing *******", "info")
    logFile.print("Log file opened", "info")
    with get_output_file(constant.FOLDER_OUTPUT, now) as outFile:
        logFile.print("Got output file", "info")

        # get files in raw folder
        raw_files = os.listdir(constant.FOLDER_RAW)
        logFile.print("Got raw files: " + str(raw_files))
        for raw in raw_files:
            raw = constant.FOLDER_RAW + "/" + raw
            logFile.print("raw: " + raw)
            process_file(raw, outFile, logFile)

        logFile.print("Closing output file", "info")
    logFile.print("--- Closing Log File", "info")
