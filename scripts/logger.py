from datetime import datetime


class Logger:
    """
    Logger class

    """

    def __init__(self, output_folder_name: str):
        """
        Initialize the logger object with the output folder name.
        :param output_folder_name: Name of the log folder
        """
        self.output_folder_name = output_folder_name
        self.log_file_name = "logs.txt"

    def __enter__(self):
        file_name = self.output_folder_name + '/' + self.log_file_name
        self.open_file = open(file_name, 'a')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.open_file.close()

    def print(self, message: str):
        now = datetime.now()
        self.open_file.write(f'{now.strftime("%d-%m-%Y, %H-%M-%S")} - {message}\n')
