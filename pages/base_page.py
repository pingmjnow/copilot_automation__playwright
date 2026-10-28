"""Shared behaviour for all page objects."""

import re

from playwright.sync_api import Page, expect

from components.side_menu import SideMenu


class BasePage:
    """Base class providing navigation, menu access, and common assertions."""

    PATH = "/"

    def __init__(self, page: Page) -> None:
        self.page = page

    @property
    def menu(self) -> SideMenu:
        return SideMenu(self.page)

    def open(self, base_url: str) -> "BasePage":
        """Navigate to this page and return the page object."""
        self.page.goto(f"{base_url.rstrip('/')}{self.PATH}")
        return self

    def expect_loaded(self) -> None:
        """Assert that the browser is currently showing this page."""
        expect(self.page).to_have_url(re.compile(rf"{re.escape(self.PATH)}$"))

    @staticmethod
    def to_amount(text: str) -> float:
        """Convert a SauceDemo money label such as "$29.99" to a float."""
        return float(re.sub(r"[^\d.]", "", text))
