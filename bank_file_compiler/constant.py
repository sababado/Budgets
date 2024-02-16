# constants
from typing import Literal

# folder names relative to this script

FOLDER_DATA = "../data"
FOLDER_RAW = "../data/raw"
FOLDER_OUTPUT = "../data/output"
FOLDER_LOGS = "../data/logs"

HEADER_TYPE_USAA: str = "USAA"
FILE_TYPE_USAA_CHECKING: str = "USAA Checking"
FILE_TYPE_USAA_SAVINGS: str = "USAA Savings"
FILE_TYPE_NFCU: str = "NFCU"
FILE_TYPE_CAPITALONE: str = "CapitalOne"
FILE_TYPE_CASH: str = "Cash"

_FILE_TYPES = Literal[
              FILE_TYPE_USAA_CHECKING:str,
              FILE_TYPE_USAA_SAVINGS,
              FILE_TYPE_CAPITALONE,
              FILE_TYPE_NFCU,
              FILE_TYPE_CASH]

CSV_OUTPUT_HEADER = "Date,Method,Description,Category,Debit,Credit,Notes,Business or Personal"

HEADER_CAPITALONE: str = "Transaction Date,Posted Date,Card No.,Description,Category,Debit,Credit"
HEADER_NFCU: str = "Date,No.,Description,Debit,Credit"
HEADER_USAA: str = "Date,Description,Original Description,Category,Amount,Status"

# This should always contain all the header types.
HEADERS = {
    FILE_TYPE_CAPITALONE: HEADER_CAPITALONE,
    FILE_TYPE_NFCU: HEADER_NFCU,
    HEADER_TYPE_USAA: HEADER_USAA
}
