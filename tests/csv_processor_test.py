from contextlib import nullcontext as does_not_raise

import pytest

from bank_file_compiler import csv_processor, constant
from bank_file_compiler.logger import Logger


@pytest.mark.parametrize("description,expected_output",
                         [
                             ("Nothing description doesnt exist", ("", "")),
                             ("ATM Fee Rebate", ("Refund", "Personal"))
                         ])
def test_map_description(description, expected_output):
    assert csv_processor.map_description(description) == expected_output


@pytest.mark.parametrize("csv_header,file_name,expected_output",
                         [
                             (["Transaction Date", "Posted Date", "Card No.", "Description", "Category", "Debit",
                               "Credit"],
                              "gobbledigook.csv", constant.FILE_TYPE_CAPITALONE),
                             (["Date", "Description", "Original Description", "Category", "Amount", "Status"],
                              "usaa checking.csv", constant.FILE_TYPE_USAA_CHECKING),
                             (["Date", "Description", "Original Description", "Category", "Amount", "Status"],
                              "usaa savings.csv", constant.FILE_TYPE_USAA_SAVINGS),
                             (["Date", "Description", "Original Description", "Category", "Amount", "Status"],
                              "usaa credit.csv", constant.FILE_TYPE_USAA_CREDIT),
                             (["Date", "Description", "Original Description", "Category", "Amount", "Status"],
                              "savings.csv", constant.FILE_TYPE_USAA_SAVINGS),
                             (["Transaction Date", "Posted Date", "Card No.", "Description", "Category", "Debit",
                               "Credit"],
                              "savings.csv", constant.FILE_TYPE_CAPITALONE),
                             (["Posting Date","Transaction Date","Amount","Credit Debit Indicator","type","Type Group","Reference","Instructed Currency","Currency Exchange Rate","Instructed Amount","Description","Category","Check Serial Number","Card Ending"],
                              "transactions.csv", constant.FILE_TYPE_NFCU),
                         ])
def test_determine_bank_type(csv_header: [str], file_name: str, expected_output: str):
    assert csv_processor.determine_bank_type(csv_header, file_name, Logger()) == expected_output


@pytest.mark.parametrize("csv_header,file_name,expectation",
                         [
                             (["Date", "Debit", "Credit"],
                              "transactions.csv", pytest.raises(Exception)),
                             (["Date", "Description", "Original Description", "Category", "Amount", "Status"],
                              "usaa checking.csv", does_not_raise()),
                         ])
def test_determine_bank_type_exception(csv_header: [str], file_name: str, expectation):
    with expectation:
        assert csv_processor.determine_bank_type(csv_header, file_name, Logger()) is not None


usaa_test_data = [
    (["2024-02-07", "Capital One", "CAPITAL ONE      MOBILE PMT ***********LHH8",
      "Credit Card Payment", "-4500.00", "Posted"],
     constant.FILE_TYPE_USAA_CHECKING,
     "2024-02-07," + constant.FILE_TYPE_USAA_CHECKING + ",CAPITAL ONE      MOBILE PMT ***********LHH8,Credit Card Payment,4500.0,,,Personal"),
    (["2025-02-07", "Capital One", "Orig Desc", "Payment", "500.00", "Posted"],
     constant.FILE_TYPE_USAA_SAVINGS,
     "2025-02-07," + constant.FILE_TYPE_USAA_SAVINGS + ",Orig Desc,Payment,,500.0,,"),
    (["2025-02-07", "Some Desc", "Stowbird Storage Description", "Payment", "500.00", "Posted"],
     constant.FILE_TYPE_USAA_SAVINGS,
     "2025-02-07," + constant.FILE_TYPE_USAA_SAVINGS + ",Stowbird Storage Description,Rent,,500.0,,Personal"),
    (["2025-02-07", "Some Desc", "Stowbird Storage Description", "Payment", "500.00", "Posted"],
     constant.FILE_TYPE_USAA_CREDIT,
     "2025-02-07," + constant.FILE_TYPE_USAA_CREDIT + ",Stowbird Storage Description,Rent,,500.0,,Personal"),
]
nfcu_test_data = [
    (["1/29/25","1/27/25","100","Debit","POS","POS","","","","","DEBIT-BDC 6187 AAW SAINT PAUL MN","Other Expenses","",""],
     constant.FILE_TYPE_NFCU,
     "2025-01-27," + constant.FILE_TYPE_NFCU + ",DEBIT-BDC 6187 AAW SAINT PAUL MN,Fees,100,,,Szabo Woodworks"),
    (["1/27/25","1/27/25","750","Credit","Transfer","Transfer","","","","","Transfer From Robert J Szabo -5818","Transfers","",""],
     constant.FILE_TYPE_NFCU,
     "2025-01-27," + constant.FILE_TYPE_NFCU + ",Transfer From Robert J Szabo -5818,,,750,,"),
]
capitalone_test_data = [
    (["2024-02-07", "2024-02-09", "7278", "WENDY'S", "Dining", "13.52", ""],
     constant.FILE_TYPE_CAPITALONE,
     "2024-02-07,7278,WENDY'S,Dining,13.52,,,"),
    (["2024-02-27", "2024-02-27", "7278", "Some Thing", "P/C", "", "666.66"],
     constant.FILE_TYPE_CAPITALONE,
     "2024-02-27,7278,Some Thing,P/C,,666.66,,"),
    (
        ["2024-02-07", "2024-02-09", "7278", "VAED TREAS 310 Long BS String", "VAED TREAS 310 Long BS String", "13.52",
         ""],
        constant.FILE_TYPE_CAPITALONE,
        "2024-02-07,7278,VAED TREAS 310 Long BS String,VA GI Bill,13.52,,,Personal"),
]


@pytest.mark.parametrize("row,bank_type,expected_output", usaa_test_data)
def test_transform_bank_data_usaa(row: [str], bank_type: str, expected_output: str):
    assert csv_processor.transform_bank_data_usaa(row, bank_type) == expected_output


@pytest.mark.parametrize("row,bank_type,expected_output", usaa_test_data + nfcu_test_data + capitalone_test_data)
def test_transform_bank_data(row: [str], bank_type: str, expected_output: str):
    assert csv_processor.transform_bank_data(row, bank_type, Logger()) == expected_output


@pytest.mark.parametrize("row,bank_type,expectation",
                         [
                             (["2024-02-07", "Capital One", "CAPITAL ONE      MOBILE PMT ***********LHH8",
                               "Credit Card Payment", "-4500.00", "Posted"],
                              constant.FILE_TYPE_USAA_CHECKING,
                              does_not_raise()),
                             (["2025-02-07", "Capital One", "Orig Desc", "Payment", "500.00", "Posted"],
                              "Unsupported Bank Type",
                              pytest.raises(Exception)),
                         ])
def test_transform_bank_data_error(row: [str], bank_type: str, expectation):
    with expectation:
        assert csv_processor.transform_bank_data(row, bank_type, Logger()) is not None
