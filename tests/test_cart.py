"""Shopping cart tests for https://www.saucedemo.com, driven by Excel data."""

import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from testdata.excel_data import load_cases

PRODUCTS = load_cases("products")


@pytest.mark.ui
@pytest.mark.smoke
def test_cart_shows_added_item(cart_page: CartPage, default_product: dict[str, str]) -> None:
    expect(cart_page.title).to_have_text("Your Cart")

    assert cart_page.item_names() == [default_product["name"]]


@pytest.mark.ui
@pytest.mark.parametrize("product", PRODUCTS)
def test_remove_product_from_cart(
    inventory_page: InventoryPage, product: dict[str, str]
) -> None:
    inventory_page.add_to_cart(product["name"])
    cart_page = inventory_page.open_cart()

    cart_page.remove(product["name"])

    cart_page.expect_empty()


@pytest.mark.ui
def test_continue_shopping_returns_to_catalogue(cart_page: CartPage) -> None:
    inventory_page = cart_page.continue_shopping()

    expect(inventory_page.title).to_have_text("Products")


@pytest.mark.ui
def test_cart_persists_items_after_visiting_catalogue(
    cart_page: CartPage, default_product: dict[str, str]
) -> None:
    inventory_page = cart_page.continue_shopping()
    cart_page = inventory_page.open_cart()

    assert cart_page.item_names() == [default_product["name"]]


@pytest.mark.ui
def test_checkout_button_opens_information_step(cart_page: CartPage) -> None:
    checkout_page = cart_page.checkout()

    expect(checkout_page.first_name_input).to_be_visible()
    expect(checkout_page.title).to_have_text("Checkout: Your Information")
