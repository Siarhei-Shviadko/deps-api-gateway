import pytest

from deps_api_gateway.api import SerializedTableCellCoordinates
from deps_api_gateway.domain.exceptions import IllegalArgument


@pytest.mark.parametrize(
    "field, value",
    [("column", 1.2), ("row", 0.7), ("column_span", 2.5), ("row_span", 3.3)],
)
def test_non_integer_rejected(field, value):
    kwargs = dict(column=0, row=0, column_span=1, row_span=1)
    kwargs[field] = value
    with pytest.raises(IllegalArgument):
        SerializedTableCellCoordinates(**kwargs)


@pytest.mark.parametrize(
    "field, value",
    [("column", -1), ("row", -1), ("column_span", -1), ("row_span", -1)],
)
def test_negative_integer_rejected(field, value):
    kwargs = dict(column=0, row=0, column_span=1, row_span=1)
    kwargs[field] = value
    with pytest.raises(IllegalArgument):
        SerializedTableCellCoordinates(**kwargs)


@pytest.mark.parametrize(
    "field, value",
    [("column_span", 0), ("row_span", 0)],
)
def test_zero_integer_for_colspan_rowspan_rejected(field, value):
    kwargs = dict(column=0, row=0, column_span=1, row_span=1)
    kwargs[field] = value
    with pytest.raises(IllegalArgument):
        SerializedTableCellCoordinates(**kwargs)


@pytest.mark.parametrize(
    "field, value",
    [("column", 0), ("row", 0), ("column_span", 1), ("row_span", 1)],
)
def test_zero_or_positive_integer_accepted(field, value):
    kwargs = dict(column=0, row=0, column_span=1, row_span=1)
    kwargs[field] = value
    try:
        SerializedTableCellCoordinates(**kwargs)
    except IllegalArgument:
        pytest.fail(f"SerializedTableCellCoordinates raised IllegalArgument unexpectedly: {field}={value}")
