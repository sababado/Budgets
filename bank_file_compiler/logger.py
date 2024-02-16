from datetime import datetime
from typing import Literal


class Logger:
    """
    Logger class

    """

    _TYPES = Literal['debug', 'info', 'warning', 'error']

    def __init__(self, output_folder_name: str = None):
        """
        Initialize the logger object with the output folder name.
        :param output_folder_name: Name of the log folder.
                                   Null if only logs to console are desired.
        """
        self.output_folder_name = output_folder_name
        self.log_file_name = "logs.csv"
        self.should_open_file = self.output_folder_name is not None

    def __enter__(self):
        self.open_file = None
        if self.should_open_file:
            file_name = self.output_folder_name + '/' + self.log_file_name
            self.open_file = open(file_name, 'a')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.should_open_file:
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
        if self.should_open_file:
            self.open_file.write(output)
        print(output)
        if log_type == 'error':
            raise Exception(output)
