"""Login tests for https://www.saucedemo.com, driven by the Excel ``users`` sheet."""

import re

import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage
from testdata.excel_data import load_cases

LOGIN_CASES = load_cases("users")


@pytest.mark.ui
@pytest.mark.smoke
def test_login_page_is_displayed(login_page: LoginPage) -> None:
    expect(login_page.username_input).to_be_visible()
    expect(login_page.password_input).to_be_visible()
    expect(login_page.login_button).to_be_visible()
    expect(login_page.page).to_have_title("Swag Labs")


@pytest.mark.ui
@pytest.mark.parametrize("case", LOGIN_CASES)
def test_login(login_page: LoginPage, case: dict[str, str]) -> None:
    login_page.login(case["username"], case["password"])

    if case["expected_result"] == "success":
        expect(login_page.page).to_have_url(re.compile(r"/inventory\.html$"))
    else:
        login_page.expect_error(case["expected_message"])
