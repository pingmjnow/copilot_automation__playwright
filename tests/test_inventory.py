"""Product catalogue tests for https://www.saucedemo.com, driven by Excel data."""

import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from testdata.excel_data import load_cases, load_rows

PRODUCTS = load_cases("products")
SORTING_CASES = load_cases("sorting")


@pytest.mark.ui
@pytest.mark.smoke
def test_inventory_lists_every_product(inventory_page: InventoryPage) -> None:
    expect(inventory_page.title).to_have_text("Products")
    expect(inventory_page.items).to_have_count(len(load_rows("products")))


@pytest.mark.ui
def test_catalogue_matches_expected_names_and_prices(inventory_page: InventoryPage) -> None:
    expected = {row["name"]: float(row["price"]) for row in load_rows("products")}
    expect(inventory_page.items).to_have_count(len(expected))

    actual = dict(zip(inventory_page.item_names(), inventory_page.item_prices()))

    assert actual == expected


@pytest.mark.ui
@pytest.mark.parametrize("product", PRODUCTS)
def test_add_product_to_cart(inventory_page: InventoryPage, product: dict[str, str]) -> None:
    inventory_page.add_to_cart(product["name"])

    inventory_page.expect_cart_count(1)
    expect(inventory_page.item(product["name"]).get_by_role("button", name="Remove")).to_be_visible()


@pytest.mark.ui
@pytest.mark.parametrize("product", PRODUCTS)
def test_remove_product_from_catalogue(
    inventory_page: InventoryPage, product: dict[str, str]
) -> None:
    inventory_page.add_to_cart(product["name"])
    inventory_page.expect_cart_count(1)

    inventory_page.remove_from_cart(product["name"])

    inventory_page.expect_cart_empty()
    expect(
        inventory_page.item(product["name"]).get_by_role("button", name="Add to cart")
    ).to_be_visible()


@pytest.mark.ui
@pytest.mark.parametrize("case", SORTING_CASES)
def test_sorting_reorders_catalogue(inventory_page: InventoryPage, case: dict[str, str]) -> None:
    inventory_page.sort_by(case["option"])
    expect(inventory_page.items.first).to_contain_text(case["expected_first_item"])

    by_price = case["expected_order"].startswith("price")
    values = inventory_page.item_prices() if by_price else inventory_page.item_names()

    assert values == sorted(values, reverse=case["expected_order"].endswith("desc"))
