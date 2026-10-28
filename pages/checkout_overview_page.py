"""Page object for checkout step two: order overview."""

from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.checkout_complete_page import CheckoutCompletePage


class CheckoutOverviewPage(BasePage):
    """The order summary with subtotal, tax, and total."""

    PATH = "/checkout-step-two.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.title = page.locator(".title")
        self.items = page.locator(".cart_item")
        self.subtotal_label = page.locator(".summary_subtotal_label")
        self.tax_label = page.locator(".summary_tax_label")
        self.total_label = page.locator(".summary_total_label")
        self.finish_button = page.locator("[data-test='finish']")
        self.cancel_button = page.locator("[data-test='cancel']")

    def totals(self) -> dict[str, float]:
        """Return the subtotal, tax, and total as floats."""
        return {
            "subtotal": self.to_amount(self.subtotal_label.inner_text()),
            "tax": self.to_amount(self.tax_label.inner_text()),
            "total": self.to_amount(self.total_label.inner_text()),
        }

    def finish(self) -> CheckoutCompletePage:
        self.finish_button.click()
        complete_page = CheckoutCompletePage(self.page)
        complete_page.expect_loaded()
        return complete_page
