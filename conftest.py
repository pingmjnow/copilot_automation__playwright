"""Shared fixtures and hooks for the SauceDemo UI and HTTP test suites.

Credentials, products, sorting rules, checkout data, and HTTP expectations all
come from ``testdata/saucedemo_test_data.xlsx`` so the suites are data-driven.
"""

import os
from pathlib import Path
from typing import Iterator

import pytest
from dotenv import load_dotenv
from playwright.sync_api import APIRequestContext, Page, Playwright

from pages.cart_page import CartPage
from pages.checkout_information_page import CheckoutInformationPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from testdata.excel_data import load_rows

load_dotenv()

DEFAULT_BASE_URL = "https://www.saucedemo.com"

REPORTS_DIR = Path(__file__).parent / "reports"
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"


@pytest.fixture(scope="session")
def base_url() -> str:
    """Base URL of the application under test."""
    return os.getenv("BASE_URL", DEFAULT_BASE_URL)


@pytest.fixture(scope="session")
def default_product() -> dict[str, str]:
    """The first product row of the ``products`` sheet."""
    return load_rows("products")[0]


@pytest.fixture(scope="session")
def valid_checkout() -> dict[str, str]:
    """The ``checkout`` row flagged with ``expected_result = success``."""
    return next(row for row in load_rows("checkout") if row["expected_result"] == "success")


@pytest.fixture(scope="session")
def username() -> str:
    """Login name of the ``standard`` user, overridable via SAUCE_USERNAME."""
    standard_user = next(row for row in load_rows("users") if row["id"] == "standard")
    return os.getenv("SAUCE_USERNAME", standard_user["username"])


@pytest.fixture(scope="session")
def password() -> str:
    """Password of the ``standard`` user, overridable via SAUCE_PASSWORD."""
    standard_user = next(row for row in load_rows("users") if row["id"] == "standard")
    return os.getenv("SAUCE_PASSWORD", standard_user["password"])


@pytest.fixture
def login_page(page: Page, base_url: str) -> LoginPage:
    """Open the login screen and hand back its page object."""
    return LoginPage(page).open(base_url)


@pytest.fixture
def inventory_page(login_page: LoginPage, username: str, password: str) -> InventoryPage:
    """Log in through the UI and return the product catalogue page."""
    return login_page.login_successfully(username, password)


@pytest.fixture
def cart_page(inventory_page: InventoryPage, default_product: dict[str, str]) -> CartPage:
    """Open the cart with the default product already added."""
    inventory_page.add_to_cart(default_product["name"])
    inventory_page.expect_cart_count(1)
    return inventory_page.open_cart()


@pytest.fixture
def checkout_information_page(cart_page: CartPage) -> CheckoutInformationPage:
    """Open checkout step one with the cart fixture already populated."""
    return cart_page.checkout()



@pytest.fixture
def api_request(playwright: Playwright, base_url: str) -> Iterator[APIRequestContext]:
    """Isolated API request context, disposed when the test finishes."""
    context = playwright.request.new_context(base_url=base_url)
    yield context
    context.dispose()


@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """Capture a full-page screenshot whenever a test fails."""
    report = yield
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if isinstance(page, Page) and not page.is_closed():
            SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=SCREENSHOTS_DIR / f"{item.name}.png", full_page=True)
    return report
