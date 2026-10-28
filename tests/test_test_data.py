"""Guards the Excel workbook that drives every parametrized suite."""

import pytest

from testdata.excel_data import DATA_FILE, SCHEMAS, load_rows


@pytest.mark.data
def test_workbook_exists() -> None:
    assert DATA_FILE.is_file(), f"Missing test data workbook: {DATA_FILE}"


@pytest.mark.data
@pytest.mark.parametrize("sheet", list(SCHEMAS))
def test_sheet_has_data_rows(sheet: str) -> None:
    assert load_rows(sheet), f"Sheet '{sheet}' has no data rows"


@pytest.mark.data
@pytest.mark.parametrize("sheet", list(SCHEMAS))
def test_sheet_row_ids_are_unique(sheet: str) -> None:
    ids = [row["id"] for row in load_rows(sheet)]

    assert len(ids) == len(set(ids)), f"Duplicate ids in sheet '{sheet}': {ids}"
