"""Page object for the checkout confirmation screen."""

from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class CheckoutCompletePage(BasePage):
    """The order confirmation shown after finishing the checkout."""

    PATH = "/checkout-complete.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.title = page.locator(".title")
        self.header = page.locator(".complete-header")
        self.text = page.locator(".complete-text")
        self.back_to_products_button = page.locator("[data-test='back-to-products']")

    def expect_order_complete(self) -> None:
        expect(self.header).to_have_text("Thank you for your order!")

    def back_to_products(self):
        """Return to the product catalogue."""
        from pages.inventory_page import InventoryPage

        self.back_to_products_button.click()
        inventory_page = InventoryPage(self.page)
        inventory_page.expect_loaded()
        return inventory_page
