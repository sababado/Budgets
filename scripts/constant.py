# constants
from typing import Literal

# folder names relative to this script

FOLDER_DATA = "../data"
FOLDER_RAW = "../data/raw"
FOLDER_OUTPUT = "../data/output"
FOLDER_LOGS = "../data/logs"

FILE_USAA: str = "USAA"
FILE_NFCU: str = "NFCU"
FILE_CAPITALONE: str = "CapitalOne"
FILE_CASH: str = "Cash"

_FILE_TYPES = Literal[FILE_USAA, FILE_CAPITALONE, FILE_NFCU, FILE_CASH]

CSV_OUTPUT_HEADER = "Date,Method,Description,Category,Debit,Credit,Notes,Business or Personal"

HEADER_CAPITALONE: str = "Transaction Date,Posted Date,Card No.,Description,Category,Debit,Credit"
HEADER_NFCU: str = "Date,No.,Description,Debit,Credit"
HEADER_USAA: str = "Date,Description,Original Description,Category,Amount,Status"

# This should always contain all the header types.
HEADERS = {
    FILE_CAPITALONE: HEADER_CAPITALONE,
    FILE_NFCU: HEADER_NFCU,
    FILE_USAA: HEADER_USAA
}
