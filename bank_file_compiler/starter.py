# Main file
import os
from datetime import datetime

import constant
import bank_file_compiler
import env_setup
from logger import Logger


def run_processor():
    now = datetime.now()
    with Logger(constant.FOLDER_LOGS) as logFile:
        logFile.print("******* Starting CSV processing *******", "info")
        logFile.print("Log file opened", "info")
        with bank_file_compiler.get_output_file(constant.FOLDER_OUTPUT, now) as outFile:
            logFile.print("Got output file", "info")

            # get files in raw folder
            raw_files = os.listdir(constant.FOLDER_RAW)
            logFile.print("Got raw files: " + str(raw_files))
            for raw in raw_files:
                raw = constant.FOLDER_RAW + "/" + raw
                logFile.print("raw: " + raw)
                bank_file_compiler.process_file(raw, outFile, logFile)

            logFile.print("Closing output file", "info")
        logFile.print("--- Closing Log File", "info")


def main():
    env_setup.init()
    run_processor()


if __name__ == '__main__':
    main()
