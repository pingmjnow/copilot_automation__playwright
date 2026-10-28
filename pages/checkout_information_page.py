"""Page object for checkout step one: shipping information."""

from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from pages.checkout_overview_page import CheckoutOverviewPage


class CheckoutInformationPage(BasePage):
    """The form collecting first name, last name, and postal code."""

    PATH = "/checkout-step-one.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.title = page.locator(".title")
        self.first_name_input = page.locator("#first-name")
        self.last_name_input = page.locator("#last-name")
        self.postal_code_input = page.locator("#postal-code")
        self.continue_button = page.locator("[data-test='continue']")
        self.cancel_button = page.locator("[data-test='cancel']")
        self.error_message = page.locator("[data-test='error']")

    def fill_information(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)

    def expect_error(self, message: str) -> None:
        expect(self.error_message).to_contain_text(message)

    def continue_to_overview(self) -> CheckoutOverviewPage:
        self.continue_button.click()
        overview_page = CheckoutOverviewPage(self.page)
        overview_page.expect_loaded()
        return overview_page

    def cancel(self):
        """Abandon the checkout and return to the cart."""
        from pages.cart_page import CartPage

        self.cancel_button.click()
        cart_page = CartPage(self.page)
        cart_page.expect_loaded()
        return cart_page
