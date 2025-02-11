# constants
import json
from typing import Literal

# folder names relative to this script

FOLDER_DATA = "../data"
FOLDER_RAW = "../data/raw"
FOLDER_OUTPUT = "../data/output"
FOLDER_LOGS = "../data/logs"
DEFAULT_CONFIG_FILE = "../config/config.json"

HEADER_TYPE_USAA: str = "USAA"
FILE_TYPE_USAA_CHECKING: str = "USAA Checking"
FILE_TYPE_USAA_SAVINGS: str = "USAA Savings"
FILE_TYPE_USAA_CREDIT: str = "USAA Credit"
FILE_TYPE_NFCU: str = "NFCU"
FILE_TYPE_CAPITALONE: str = "CapitalOne"
FILE_TYPE_CASH: str = "Cash"

_FILE_TYPES = Literal[
              FILE_TYPE_USAA_CHECKING:str,
              FILE_TYPE_USAA_CREDIT,
              FILE_TYPE_USAA_SAVINGS,
              FILE_TYPE_CAPITALONE,
              FILE_TYPE_NFCU,
              FILE_TYPE_CASH]

CSV_OUTPUT_HEADER = "Date,Method,Description,Category,Debit,Credit,Notes,Business or Personal"

HEADER_CAPITALONE: str = "Transaction Date,Posted Date,Card No.,Description,Category,Debit,Credit"
HEADER_NFCU: str = "Posting Date,Transaction Date,Amount,Credit Debit Indicator,type,Type Group,Reference,Instructed Currency,Currency Exchange Rate,Instructed Amount,Description,Category,Check Serial Number,Card Ending"
HEADER_USAA: str = "Date,Description,Original Description,Category,Amount,Status"

# This should always contain all the header types.
HEADERS = {
    FILE_TYPE_CAPITALONE: HEADER_CAPITALONE,
    FILE_TYPE_NFCU: HEADER_NFCU,
    HEADER_TYPE_USAA: HEADER_USAA
}

with open(DEFAULT_CONFIG_FILE, 'r') as config_file:
    config_file = json.load(config_file)
    MAP_CATEGORY = config_file["categoryMap"]
    MAP_BUSINESS_OR_PERSONAL = config_file["businessOrPersonalMap"]
