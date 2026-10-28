"""Page object for the SauceDemo shopping cart."""

from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from pages.checkout_information_page import CheckoutInformationPage


class CartPage(BasePage):
    """The cart summary listing every selected product."""

    PATH = "/cart.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.title = page.locator(".title")
        self.items = page.locator(".cart_item")
        self.item_names_locator = page.locator(".inventory_item_name")
        self.continue_shopping_button = page.locator("[data-test='continue-shopping']")
        self.checkout_button = page.locator("[data-test='checkout']")

    def item_names(self) -> list[str]:
        return self.item_names_locator.all_inner_texts()

    def remove(self, name: str) -> None:
        self.items.filter(has_text=name).get_by_role("button", name="Remove").click()

    def expect_empty(self) -> None:
        expect(self.items).to_have_count(0)

    def continue_shopping(self):
        """Return to the product catalogue."""
        from pages.inventory_page import InventoryPage

        self.continue_shopping_button.click()
        inventory_page = InventoryPage(self.page)
        inventory_page.expect_loaded()
        return inventory_page

    def checkout(self) -> CheckoutInformationPage:
        self.checkout_button.click()
        checkout_page = CheckoutInformationPage(self.page)
        checkout_page.expect_loaded()
        return checkout_page
