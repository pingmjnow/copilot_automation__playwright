"""Page object for the SauceDemo login screen."""

from typing import TYPE_CHECKING

from playwright.sync_api import Page, expect

from pages.base_page import BasePage

if TYPE_CHECKING:
    from pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    """The SauceDemo login form at the site root."""

    PATH = "/"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username_input = page.locator("[data-test='username']")
        self.password_input = page.locator("[data-test='password']")
        self.login_button = page.locator("[data-test='login-button']")
        self.error_message = page.locator("[data-test='error']")

    def open(self, base_url: str) -> "LoginPage":
        super().open(base_url)
        return self

    def login(self, username: str, password: str) -> None:
        """Fill the credentials and submit the form."""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def login_successfully(self, username: str, password: str) -> "InventoryPage":
        """Log in and return the inventory page object."""
        from pages.inventory_page import InventoryPage

        self.login(username, password)
        inventory_page = InventoryPage(self.page)
        inventory_page.expect_loaded()
        return inventory_page

    def expect_error(self, message: str) -> None:
        """Assert that the error banner contains the expected text."""
        expect(self.error_message).to_contain_text(message)
