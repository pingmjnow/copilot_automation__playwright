"""The burger menu shown on every authenticated SauceDemo page."""

from playwright.sync_api import Page, expect


class SideMenu:
    """Locators and actions for the navigation drawer."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.open_button = page.locator("#react-burger-menu-btn")
        self.close_button = page.locator("#react-burger-cross-btn")
        self.all_items_link = page.locator("#inventory_sidebar_link")
        self.about_link = page.locator("#about_sidebar_link")
        self.logout_link = page.locator("#logout_sidebar_link")
        self.reset_app_state_link = page.locator("#reset_sidebar_link")

    def open(self) -> "SideMenu":
        self.open_button.click()
        expect(self.logout_link).to_be_visible()
        return self

    def logout(self):
        """Log out and return to the login page."""
        from pages.login_page import LoginPage

        self.open().logout_link.click()
        return LoginPage(self.page)

    def reset_app_state(self) -> None:
        """Clear the cart and the application state, then close the menu."""
        self.open().reset_app_state_link.click()
        expect(self.reset_app_state_link).to_be_visible()
        self.close_button.click()
