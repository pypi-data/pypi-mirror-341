from typing import Any, ClassVar
from unittest.mock import patch

import pytest

from flexible_schema import Schema, SchemaValidationError, TableValidationError


def get_sample_schema(allow_extra_columns: bool) -> Schema:
    class Sample(Schema[type, dict[str, type], dict[str, Any]]):
        allow_extra_columns: ClassVar[bool]
        subject_id: int
        foo: str | None = None

        @classmethod
        def map_type(cls, field_type: Any) -> Any:
            return field_type

        @classmethod
        def schema(cls):
            return {c.name: c.dtype for c in cls._columns()}

        @classmethod
        def _raw_schema_col_type(cls, schema: Any, col: str) -> Any:
            return schema[col]

        @classmethod
        def _raw_table_schema(cls, table: dict) -> Any:
            return {k: type(v) for k, v in table.items()}

        @classmethod
        def _raw_schema_cols(cls, schema: Any) -> list[str]:
            return list(schema.keys())

        @classmethod
        def _reorder_raw_table(cls, tbl: dict, tbl_order: list[str]) -> dict:
            return {k: tbl[k] for k in tbl_order}

        @classmethod
        def _cast_raw_table_column(cls, tbl: dict, col: str, col_type: Any) -> dict:
            out = {**tbl}
            out[col] = col_type(tbl[col])
            return out

        @classmethod
        def _is_raw_table(cls, arg: Any) -> bool:
            return isinstance(arg, dict)

        @classmethod
        def _any_null(cls, tbl: dict, col: str) -> bool:
            return tbl.get(col) is None

        _all_null = _any_null

    Sample.allow_extra_columns = allow_extra_columns

    return Sample


def test_schema_with_extra_cols():
    Sample = get_sample_schema(True)  # noqa: N806

    assert Sample.schema() == {"subject_id": int, "foo": str}

    sample = Sample(subject_id=1)
    assert sample["subject_id"] == 1
    assert sample.to_dict() == {"subject_id": 1}
    assert list(sample.keys()) == ["subject_id"]
    assert list(sample.items()) == [("subject_id", 1)]
    assert list(sample) == ["subject_id"]
    assert list(sample.values()) == [1]

    assert sample == Sample(subject_id=1)
    assert sample == Sample(1)

    sample_2 = Sample(subject_id=1, foo="bar")
    assert sample != sample_2
    assert sample_2["foo"] == "bar"
    assert sample_2.to_dict() == {"subject_id": 1, "foo": "bar"}
    assert sample_2 == Sample.from_dict({"subject_id": 1, "foo": "bar"})

    sample["foo"] = "bar"
    assert sample == sample_2

    sample_3 = Sample(subject_id=1, foo="bar", extra="extra")
    assert sample_3["extra"] == "extra"
    assert sample_3.to_dict() == {"subject_id": 1, "foo": "bar", "extra": "extra"}
    assert sample_3 == Sample.from_dict(sample_3.to_dict())

    assert sample_3 == Sample(1, "bar", extra="extra")

    assert list(sample_3.keys()) == ["subject_id", "foo", "extra"]
    assert list(sample_3.items()) == [
        ("subject_id", 1),
        ("foo", "bar"),
        ("extra", "extra"),
    ]
    assert list(sample_3) == ["subject_id", "foo", "extra"]
    assert list(sample_3.values()) == [1, "bar", "extra"]

    sample["extra"] = "extra"
    assert sample == sample_3


def test_schema_no_extra_cols():
    Sample = get_sample_schema(False)  # noqa: N806

    sample = Sample(subject_id=1)
    assert sample.to_dict() == {"subject_id": 1}

    sample_2 = Sample(subject_id=1, foo="bar")
    assert sample_2.to_dict() == {"subject_id": 1, "foo": "bar"}

    sample["foo"] = "bar"
    assert sample == sample_2

    with pytest.raises(SchemaValidationError) as excinfo:
        sample = Sample(subject_id=1, foo="bar", extra="extra")
    assert "Sample does not allow extra columns, but got: 'extra'" in str(excinfo.value)

    with pytest.raises(SchemaValidationError) as excinfo:
        sample["extra"] = "extra"
    assert "Extra field not allowed: 'extra'" in str(excinfo.value)


def test_errors():
    Sample = get_sample_schema(False)  # noqa: N806

    with pytest.raises(TypeError) as excinfo:
        Sample(1, 2, 3)
    assert "Sample expected 2 arguments, got 3" in str(excinfo.value)

    with pytest.raises(TypeError) as excinfo:
        Sample(1, subject_id=1, foo=2)
    assert "Sample got multiple values for argument 'subject_id'" in str(excinfo.value)


def test_more_errors():
    Sample = get_sample_schema(False)  # noqa: N806

    with patch.object(Sample, "_validate_schema", side_effect=ValueError):
        with pytest.raises(SchemaValidationError) as excinfo:
            Sample.validate({"subject_id": 1, "foo": "bar"})
        assert "Schema validation failed" in str(excinfo.value)

    with patch.object(Sample, "_validate_schema", side_effect=SchemaValidationError("No-details")):
        with pytest.raises(SchemaValidationError) as excinfo:
            Sample.align({"subject_id": 1, "foo": "bar"})
        assert "No-details" in str(excinfo.value)

    Sample._is_raw_schema = lambda x: False
    Sample._is_raw_table = lambda x: True
    with patch.object(Sample, "_validate_table", side_effect=ValueError):
        with pytest.raises(TableValidationError) as excinfo:
            Sample.validate({"subject_id": 1, "foo": "bar"})
        assert "Table validation failed" in str(excinfo.value)
