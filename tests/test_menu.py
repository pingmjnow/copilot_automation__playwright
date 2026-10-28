"""Navigation menu tests for https://www.saucedemo.com, driven by Excel data."""

import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from testdata.excel_data import load_cases

PRODUCTS = load_cases("products")


@pytest.mark.ui
@pytest.mark.regression
def test_logout_returns_to_login_page(inventory_page: InventoryPage) -> None:
    login_page = inventory_page.menu.logout()

    expect(login_page.login_button).to_be_visible()
    assert isinstance(login_page, LoginPage)


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize("product", PRODUCTS)
def test_reset_app_state_clears_cart(
    inventory_page: InventoryPage, product: dict[str, str]
) -> None:
    inventory_page.add_to_cart(product["name"])
    inventory_page.expect_cart_count(1)

    inventory_page.menu.reset_app_state()

    inventory_page.expect_cart_empty()


@pytest.mark.ui
@pytest.mark.regression
def test_all_items_link_returns_to_catalogue(cart_page, base_url: str) -> None:
    cart_page.menu.open().all_items_link.click()

    expect(cart_page.page).to_have_url(f"{base_url}/inventory.html")
