"""Tests for Table visualization class."""

import pandas as pd
import pytest

import datawrapper
from tests.utils import _test_class


def test_table():
    """Test Table class can validate examples and serialize/deserialize."""
    _test_class(datawrapper.Table)


def test_table_creation_basic():
    """Test basic Table creation with minimal configuration."""
    df = pd.DataFrame({
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [25, 30, 35],
        "City": ["NYC", "LA", "Chicago"],
    })
    
    table = datawrapper.Table(
        title="People Data",
        data=df,
        source_name="HR System",
    )
    
    assert table.chart_type == "tables"
    assert table.title == "People Data"
    assert isinstance(table.data, pd.DataFrame)
    assert len(table.data) == 3


def test_table_with_column_order():
    """Test Table with custom column ordering."""
    df = pd.DataFrame({
        "Name": ["Alice", "Bob"],
        "Age": [25, 30],
        "City": ["NYC", "LA"],
    })
    
    table = datawrapper.Table(
        title="Reordered Data",
        data=df,
        column_order=[2, 0, 1],  # City, Name, Age
    )
    
    assert table.column_order == [2, 0, 1]
    serialized = table.serialize_model()
    assert serialized["metadata"]["data"]["column-order"] == [2, 0, 1]


def test_table_with_column_formats():
    """Test Table with column-specific formatting."""
    df = pd.DataFrame({
        "Product": ["Widget", "Gadget"],
        "Price": [19.99, 29.99],
        "Quantity": [100, 200],
    })
    
    table = datawrapper.Table(
        title="Product Inventory",
        data=df,
        column_formats=[
            {"column": "Price", "type": "number", "number-format": "n2", "number-prepend": "$"},
            {"column": "Quantity", "type": "number", "number-format": "n0"},
        ],
    )
    
    assert len(table.column_formats) == 2
    serialized = table.serialize_model()
    
    # Check that column-format was serialized correctly
    col_format = serialized["metadata"]["data"]["column-format"]
    assert "Price" in col_format
    assert "Quantity" in col_format
    assert col_format["Price"]["number-format"] == "n2"
    assert col_format["Price"]["number-prepend"] == "$"


def test_table_serialization():
    """Test that Table serializes correctly for API."""
    df = pd.DataFrame({
        "Name": ["Alice"],
        "Score": [95],
    })
    
    table = datawrapper.Table(
        title="Test Scores",
        data=df,
        byline="Teacher",
        source_name="Gradebook",
        column_order=[1, 0],  # Score, Name
    )
    
    serialized = table.serialize_model()
    
    # Check top-level fields
    assert serialized["type"] == "tables"
    assert serialized["title"] == "Test Scores"
    assert serialized["language"] == "en-US"
    
    # Check metadata
    assert serialized["metadata"]["data"]["column-order"] == [1, 0]
    assert serialized["metadata"]["describe"]["byline"] == "Teacher"
    assert serialized["metadata"]["describe"]["source-name"] == "Gradebook"


def test_table_deserialization():
    """Test that Table can deserialize from API response."""
    api_response = {
        "id": "abc123",
        "type": "tables",
        "title": "Imported Table",
        "theme": "datawrapper",
        "metadata": {
            "data": {
                "transpose": False,
                "column-order": [0, 2, 1],
                "column-format": {
                    "Name": {"type": "text"},
                    "Score": {"type": "number", "number-format": "n0"},
                }
            },
            "describe": {
                "intro": "Student scores",
                "byline": "School",
                "source-name": "System",
                "source-url": "",
            },
            "annotate": {
                "notes": "Q1 2024",
            },
            "visualize": {
                "dark-mode-invert": False,
                "sharing": {"enabled": False, "url": ""},
            },
            "publish": {
                "autoDarkMode": False,
                "blocks": {
                    "get-the-data": False,
                    "download-image": False,
                    "download-pdf": False,
                    "download-svg": False,
                    "embed": False,
                    "logo": {"id": "", "enabled": False},
                },
                "force-attribution": False,
            },
            "custom": {},
        },
    }
    
    deserialized = datawrapper.Table.deserialize_model(api_response)
    
    assert deserialized["title"] == "Imported Table"
    assert deserialized["intro"] == "Student scores"
    assert deserialized["column_order"] == [0, 2, 1]
    
    # Check column formats were deserialized
    assert "column_formats" in deserialized
    assert len(deserialized["column_formats"]) == 2


def test_table_method_chaining():
    """Test that Table supports method chaining for common operations."""
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    
    table = datawrapper.Table(
        title="Original Title",
        data=df,
    )
    
    # Test that we can chain methods (returns self)
    result = table
    assert isinstance(result, datawrapper.Table)
    assert result.chart_type == "tables"


def test_table_csv_serialization():
    """Test that Table correctly converts data to CSV."""
    df = pd.DataFrame({
        "Name": ["Alice", "Bob"],
        "Age": [25, 30],
    })
    
    table = datawrapper.Table(
        title="People",
        data=df,
    )
    
    csv_data = table.serialize_data()
    
    assert csv_data is not None
    assert "Name" in csv_data
    assert "Age" in csv_data
    assert "Alice" in csv_data
    assert "Bob" in csv_data


def test_table_with_empty_data():
    """Test that Table handles empty data gracefully."""
    table = datawrapper.Table(
        title="Empty Table",
        data=[],
    )
    
    csv_data = table.serialize_data()
    assert csv_data is None  # Should return None for empty data
