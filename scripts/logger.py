from datetime import datetime
from typing import Literal


class Logger:
    """
    Logger class

    """

    _TYPES = Literal['debug', 'info', 'warning', 'error']

    def __init__(self, output_folder_name: str):
        """
        Initialize the logger object with the output folder name.
        :param output_folder_name: Name of the log folder
        """
        self.output_folder_name = output_folder_name
        self.log_file_name = "logs.csv"

    def __enter__(self):
        file_name = self.output_folder_name + '/' + self.log_file_name
        self.open_file = open(file_name, 'a')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.open_file.close()

    def print(self, message: str, log_type: _TYPES = "debug"):
        """
        Print a message to the log file. Comes with a datetime stamp.
        :param message: Message to print.
        :param log_type:
        :return:
        """
        now = datetime.now()
        output = f'{now.strftime("%d-%m-%Y %H-%M-%S")},{log_type},{message}\n'
        self.open_file.write(output)
        print(output)
