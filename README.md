# SauceDemo Test Automation Framework

[![Smoke tests](https://github.com/pingmjnow/copilot_automation__playwright/actions/workflows/smoke.yml/badge.svg)](https://github.com/pingmjnow/copilot_automation__playwright/actions/workflows/smoke.yml)

UI and HTTP test suite for [SauceDemo](https://www.saucedemo.com), built with **Playwright (sync API) + Pytest**.
Tests follow the Page Object Model and are driven by an Excel test-data workbook, so new cases are data changes
rather than code changes.

**Current baseline: 63 tests** (48 UI, 4 HTTP, 11 data-integrity checks).

---

## Tech stack

| Concern | Tool |
|---|---|
| Browser automation | `playwright` (sync API) |
| Test runner | `pytest` + `pytest-playwright` |
| Parallelism / timeouts | `pytest-xdist`, `pytest-timeout` |
| Reporting | `pytest-html` (HTML), built-in JUnit XML, failure screenshots |
| Test data | `openpyxl` reading `testdata/saucedemo_test_data.xlsx` |
| Config | `python-dotenv` (`.env`) + environment variables |

---

## Quick start

```bash
git clone https://github.com/pingmjnow/copilot_automation__playwright.git
cd copilot_automation__playwright
```

```powershell
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m playwright install chromium
python -m pytest -m smoke -q
```

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
python -m pytest -m smoke -q
```

Expected output: `7 passed, 56 deselected`.

---

## Project layout

```
.
├── .github/workflows/smoke.yml   # CI: smoke suite on push and pull request
├── components/
│   └── side_menu.py              # burger menu shared by every authenticated page
├── pages/
│   ├── base_page.py              # navigation, URL assertion, money parsing
│   ├── login_page.py             # / — credentials, error banner
│   ├── inventory_page.py         # /inventory.html — catalogue, sort, add/remove
│   ├── cart_page.py              # /cart.html
│   ├── checkout_information_page.py   # /checkout-step-one.html
│   ├── checkout_overview_page.py      # /checkout-step-two.html
│   └── checkout_complete_page.py      # /checkout-complete.html
├── tests/
│   ├── test_login.py             # 5 tests  (users sheet)
│   ├── test_inventory.py         # 18 tests (products + sorting sheets)
│   ├── test_cart.py              # 10 tests
│   ├── test_checkout.py          # 7 tests  (checkout sheet)
│   ├── test_menu.py              # 8 tests
│   ├── test_api.py               # 4 tests  (http_checks sheet)
│   └── test_test_data.py         # 11 tests — guards the workbook itself
├── testdata/
│   ├── excel_data.py             # cached, schema-validated loader
│   └── saucedemo_test_data.xlsx  # users, products, sorting, checkout, http_checks
├── conftest.py                   # fixtures + failure-screenshot hook
├── pytest.ini                    # markers, strict config, reports, timeout
├── requirements.txt
└── reports/                      # generated (git-ignored, .gitkeep only)
```

---

## Running tests

| Command | What it runs |
|---|---|
| `pytest` | Everything (63 tests) |
| `pytest -m smoke` | Fast gate: login, catalogue, add-to-cart, cart, checkout, HTTP checks |
| `pytest -m api` | HTTP-level checks only, no browser |
| `pytest -m data` | Excel workbook validation |
| `pytest -m ui` | All browser tests |
| `pytest -m regression` | Secondary flows (menu, logout, reset) |
| `pytest -n auto` | Parallel execution (pytest-xdist) |
| `pytest --headed --slowmo 500` | Watch the browser |
| `pytest tests/test_checkout.py -k totals` | Single test selection |

Reports are written to `reports/report.html` (self-contained) and `reports/junit.xml`;
failure screenshots go to `reports/screenshots/`. Run pytest **from the repository root** —
the report paths in `pytest.ini` are relative to the invocation directory.

---

## Test data

`testdata/saucedemo_test_data.xlsx`

| Sheet | Rows | Drives |
|---|---|---|
| `users` | 4 | valid, locked-out, invalid, and empty login attempts |
| `products` | 6 | catalogue price check, add/remove in inventory, cart and menu flows |
| `sorting` | 4 | price asc/desc, name asc/desc |
| `checkout` | 3 | valid submission + two required-field validations |
| `http_checks` | 3 | endpoint status, content type, expected text |
| `README` | — | column documentation |

Each row's `id` becomes the pytest parameter id, so `users` row `locked_out` runs as
`test_login[chromium-locked_out]`. **To add a case, add a row** — no code changes, no duplicate files.

Configuration can be overridden without touching the workbook:

```bash
BASE_URL=https://www.saucedemo.com
SAUCE_USERNAME=standard_user
SAUCE_PASSWORD=secret_sauce
```

Put these in a `.env` file (git-ignored) or set them in CI. Credentials committed to the workbook are
SauceDemo's public demo accounts, not real secrets.

---

## Configuration notes

- **Markers** are strict (`--strict-markers`): `ui`, `api`, `smoke`, `regression`, `data`.
- **Global test timeout** is 120 s (`pytest-timeout`), so a stuck navigation fails instead of hanging CI.
- **Fixtures** chain as `login_page → inventory_page → cart_page → checkout_information_page`; each test gets a
  fresh browser context, so cart state never leaks between tests.
- **Failure diagnostics**: the `pytest_runtest_makereport` hook saves a full-page screenshot on failure.

---

## Continuous integration

`.github/workflows/smoke.yml` runs the smoke suite on every push to `main` and on every pull request:

1. installs `requirements.txt` (pip cache enabled)
2. installs Chromium via `python -m playwright install --with-deps chromium`
3. runs `python -m pytest -m smoke -q`
4. uploads `reports/` as a build artifact (always, so failures are debuggable)

CI uses Python 3.13; adjust `python-version` in the workflow if you standardise elsewhere.

---

## Known limitations / roadmap

Honest list — these are deliberate next steps, not hidden gaps:

- Page readiness is asserted mainly by URL; list reads that use `all_inner_texts()` could race the SPA render.
  Plan: content-based `expect_loaded()` per page and web-first list assertions.
- Locators mix `data-test` with CSS classes; plan: standardise on `data-test` everywhere.
- The `name_asc` sorting case matches the app default, so it is a weak oracle on its own.
- Login happens through the UI per test; plan: reuse a session-scoped `storage_state` to cut runtime.
- SauceDemo's broken personas (`problem_user`, `performance_glitch_user`, `error_user`) are not covered yet.
