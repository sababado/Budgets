from contextlib import nullcontext as does_not_raise

import pytest

from bank_file_compiler import csv_processor, constant
from bank_file_compiler.logger import Logger


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
                              "savings.csv", constant.FILE_TYPE_USAA_SAVINGS),
                             (["Transaction Date", "Posted Date", "Card No.", "Description", "Category", "Debit",
                               "Credit"],
                              "savings.csv", constant.FILE_TYPE_CAPITALONE),
                             (["Date", "No.", "Description", "Debit", "Credit"],
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


@pytest.mark.parametrize("row,usaa_bank_type,expected_output",
                         [
                             (["2024-02-07", "Capital One", "CAPITAL ONE      MOBILE PMT ***********LHH8",
                               "Credit Card Payment", "-4500.00", "Posted"],
                              constant.FILE_TYPE_USAA_CHECKING,
                              "2024-02-07," + constant.FILE_TYPE_USAA_CHECKING + ",CAPITAL ONE      MOBILE PMT ***********LHH8,Credit Card Payment,4500.0,,,"),
                             (["2025-02-07", "Capital One", "Orig Desc", "Payment", "500.00", "Posted"],
                              constant.FILE_TYPE_USAA_SAVINGS,
                              "2025-02-07," + constant.FILE_TYPE_USAA_SAVINGS + ",Orig Desc,Payment,,500.0,,"),
                         ])
def test_transform_bank_data_usaa(row: [str], usaa_bank_type: str, expected_output: str):
    assert csv_processor.transform_bank_data_usaa(row, usaa_bank_type) == expected_output
