"""Checkout flow tests for https://www.saucedemo.com, driven by Excel data."""

import re

import pytest
from playwright.sync_api import expect

from pages.checkout_information_page import CheckoutInformationPage
from testdata.excel_data import load_cases, load_rows

CHECKOUT_CASES = load_cases("checkout")


def fill_information(page: CheckoutInformationPage, case: dict[str, str]) -> None:
    page.fill_information(case["first_name"], case["last_name"], case["postal_code"])


@pytest.mark.ui
@pytest.mark.smoke
def test_complete_order(
    checkout_information_page: CheckoutInformationPage, valid_checkout: dict[str, str]
) -> None:
    fill_information(checkout_information_page, valid_checkout)
    overview_page = checkout_information_page.continue_to_overview()
    expect(overview_page.items).to_have_count(1)

    complete_page = overview_page.finish()

    complete_page.expect_order_complete()
    expect(complete_page.title).to_have_text("Checkout: Complete!")


@pytest.mark.ui
@pytest.mark.parametrize("case", CHECKOUT_CASES)
def test_information_step_validation(
    checkout_information_page: CheckoutInformationPage, case: dict[str, str]
) -> None:
    fill_information(checkout_information_page, case)
    checkout_information_page.continue_button.click()

    if case["expected_result"] == "success":
        expect(checkout_information_page.page).to_have_url(re.compile(r"/checkout-step-two\.html$"))
    else:
        checkout_information_page.expect_error(case["expected_message"])


@pytest.mark.ui
def test_overview_total_equals_subtotal_plus_tax(
    checkout_information_page: CheckoutInformationPage, valid_checkout: dict[str, str]
) -> None:
    fill_information(checkout_information_page, valid_checkout)
    overview_page = checkout_information_page.continue_to_overview()

    totals = overview_page.totals()

    assert totals["total"] == pytest.approx(totals["subtotal"] + totals["tax"], abs=0.01)


@pytest.mark.ui
def test_cancel_checkout_returns_to_cart(
    checkout_information_page: CheckoutInformationPage,
) -> None:
    cart_page = checkout_information_page.cancel()

    expect(cart_page.title).to_have_text("Your Cart")


@pytest.mark.ui
def test_back_to_products_after_order(
    checkout_information_page: CheckoutInformationPage, valid_checkout: dict[str, str]
) -> None:
    fill_information(checkout_information_page, valid_checkout)
    complete_page = checkout_information_page.continue_to_overview().finish()

    inventory_page = complete_page.back_to_products()

    expect(inventory_page.items).to_have_count(len(load_rows("products")))
