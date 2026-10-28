"""HTTP-level tests using Playwright's APIRequestContext.

SauceDemo is a single-page React app with no JSON API: the server returns an
empty ``#root`` shell and the UI is rendered client-side, so the markup itself
is covered by the UI suites. The endpoints checked here come from the Excel
``http_checks`` sheet.
"""

import re

import pytest
from playwright.sync_api import APIRequestContext

from testdata.excel_data import load_cases

HTTP_CHECKS = load_cases("http_checks")


@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.parametrize("check", HTTP_CHECKS)
def test_endpoint_responds(api_request: APIRequestContext, check: dict[str, str]) -> None:
    response = api_request.get(check["path"])

    assert response.status == int(check["expected_status"]), f"Unexpected status {response.status}"
    assert check["expected_content_type"] in response.headers.get("content-type", "")
    if check["expected_text"]:
        assert check["expected_text"] in response.text()


@pytest.mark.api
def test_application_bundle_is_served(api_request: APIRequestContext) -> None:
    bundle_path = re.search(r'(/assets/[^"\']+\.js)', api_request.get("/").text()).group(1)

    response = api_request.get(bundle_path)

    assert response.ok, f"Unexpected status {response.status}"
    assert "javascript" in response.headers.get("content-type", "")
