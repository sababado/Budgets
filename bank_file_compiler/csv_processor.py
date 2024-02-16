# csv processor
import csv
import os
from datetime import datetime
from typing import TextIO

from bank_file_compiler import constant
from bank_file_compiler.logger import Logger


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


def determine_bank_type(csv_header: [str], file_name: str, log_file: Logger):
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
                    found_header = constant.FILE_TYPE_USAA_SAVINGS
                else:
                    found_header = constant.FILE_TYPE_USAA_CHECKING

            log_file.print("%% Found header: " + found_header)
            return found_header
    log_file.print("%% Could not find any matching header: " + str(csv_header), 'error')


def transform_bank_data_usaa(row: list[str], usaa_bank_type: str):
    """ Specific processing of bank data from USAA files. Checking and Savings statements are the same.
    :param row: row of bank data
    :param usaa_bank_type: USAA bank type
    :return: String of transformed data.
    """
    amount = float(row[4])
    debit_credit_val: str = ''
    if amount < 0:
        debit_credit_val = str(abs(amount)) + ","
    else:
        debit_credit_val = "," + str(amount)

    return str.format("%s,%s,%s,%s,%s,,"
                      % (row[0], usaa_bank_type, row[2], row[3], debit_credit_val))


def transform_bank_data(bank_type, log_file, row):
    # Act on the bank type
    log_file.print("%-- Processing row: " + bank_type + ": " + str(row))
    # Capital One
    if bank_type == constant.FILE_TYPE_CAPITALONE:
        return str.format("%s,%s,%s,%s,%s,,"
                          % (row[0], row[2], row[3], row[4], row[5]))
    # NFCU
    elif bank_type == constant.FILE_TYPE_NFCU:
        return str.format("%s,%s,%s,,%s,%s,,"
                          % (row[0], bank_type, row[2], row[3], row[4]))
    # USAA
    elif bank_type == constant.FILE_TYPE_USAA_CHECKING or bank_type == constant.FILE_TYPE_USAA_SAVINGS:
        return transform_bank_data_usaa(row, bank_type)
    # Uh Oh
    else:
        message: str = "****** Unsupported Bank Type: " + bank_type
        log_file.print(message)
        raise NotImplementedError(message)


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
                bank_type = determine_bank_type(row, file_name, log_file)
                log_file.print("% Found bank type: " + str(bank_type), "info")
            else:
                output_file.write(transform_bank_data(bank_type, log_file, row) + "\n")