"""Page object for the SauceDemo product catalogue."""

from playwright.sync_api import Locator, Page, expect

from pages.base_page import BasePage
from pages.cart_page import CartPage


class InventoryPage(BasePage):
    """The product list shown after a successful login."""

    PATH = "/inventory.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.title = page.locator(".title")
        self.items = page.locator(".inventory_item")
        self.item_names_locator = page.locator(".inventory_item_name")
        self.item_prices_locator = page.locator(".inventory_item_price")
        self.sort_select = page.locator("[data-test='product-sort-container']")
        self.cart_link = page.locator(".shopping_cart_link")
        self.cart_badge = page.locator(".shopping_cart_badge")

    def item(self, name: str) -> Locator:
        """Return the product card whose text contains ``name``."""
        return self.items.filter(has_text=name)

    def expect_loaded(self) -> None:
        super().expect_loaded()
        expect(self.title).to_have_text("Products")

    def add_to_cart(self, name: str) -> None:
        self.item(name).get_by_role("button", name="Add to cart").click()

    def remove_from_cart(self, name: str) -> None:
        self.item(name).get_by_role("button", name="Remove").click()

    def expect_cart_count(self, expected: int) -> None:
        expect(self.cart_badge).to_have_text(str(expected))

    def expect_cart_empty(self) -> None:
        expect(self.cart_badge).to_have_count(0)

    def sort_by(self, option: str) -> None:
        """Sort the catalogue by az, za, lohi (price asc) or hilo (price desc)."""
        self.sort_select.select_option(option)
        expect(self.sort_select).to_have_value(option)

    def item_names(self) -> list[str]:
        return self.item_names_locator.all_inner_texts()

    def item_prices(self) -> list[float]:
        return [self.to_amount(text) for text in self.item_prices_locator.all_inner_texts()]

    def open_cart(self) -> CartPage:
        self.cart_link.click()
        cart_page = CartPage(self.page)
        cart_page.expect_loaded()
        return cart_page
