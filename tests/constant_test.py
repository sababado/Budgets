import pytest

from bank_file_compiler import constant


def test_constant_test():
    assert constant.MAP_CATEGORY is not None
    assert constant.MAP_CATEGORY["ATM Fee Rebate"] == "Refund"

    assert constant.MAP_BUSINESS_OR_PERSONAL is not None
    assert constant.MAP_BUSINESS_OR_PERSONAL["ATM Fee Rebate"] == "Personal"
