"""Integration tests for Narwhals dataframe support (Polars, PyArrow, etc.)"""

from __future__ import annotations

import pytest

try:
    import polars as pl

    HAS_POLARS = True
except ImportError:
    HAS_POLARS = False


@pytest.mark.skipif(not HAS_POLARS, reason="Polars not installed")
class TestPolarsDataFrameSupport:
    """Test that charts work with Polars DataFrames via Narwhals."""

    def test_bar_chart_with_polars(self):
        """Test creating a BarChart with Polars DataFrame."""
        from datawrapper.charts import BarChart

        # Create a Polars DataFrame
        df = pl.DataFrame(
            {"Country": ["USA", "China", "India"], "Population": [331, 1411, 1380]}
        )

        # Create a chart with Polars data
        chart = BarChart(
            title="World Population",
            data=df,
        )

        # Verify the chart was created with the correct data
        assert chart.title == "World Population"
        assert chart.data is not None

        # Verify serialization works
        csv_output = chart.serialize_data()
        assert csv_output is not None
        assert "Country,Population" in csv_output
        assert "USA,331" in csv_output

    def test_line_chart_with_polars(self):
        """Test creating a LineChart with Polars DataFrame."""
        from datawrapper.charts import LineChart

        # Create a Polars DataFrame
        df = pl.DataFrame(
            {
                "Year": [2020, 2021, 2022, 2023],
                "Temperature": [14.8, 14.9, 15.1, 15.2],
            }
        )

        # Create a chart with Polars data
        chart = LineChart(
            title="Global Temperature Trend",
            data=df,
        )

        # Verify the chart was created
        assert chart.title == "Global Temperature Trend"
        assert chart.data is not None

        # Verify serialization works
        csv_output = chart.serialize_data()
        assert csv_output is not None
        assert "Year,Temperature" in csv_output

    def test_column_chart_with_polars(self):
        """Test creating a ColumnChart with Polars DataFrame."""
        from datawrapper.charts import ColumnChart

        # Create a Polars DataFrame
        df = pl.DataFrame({"Month": ["Jan", "Feb", "Mar"], "Sales": [100, 150, 120]})

        # Create a chart with Polars data
        chart = ColumnChart(
            title="Monthly Sales",
            data=df,
        )

        # Verify the chart was created
        assert chart.title == "Monthly Sales"
        assert chart.data is not None

        # Verify serialization works
        csv_output = chart.serialize_data()
        assert csv_output is not None
        assert "Month,Sales" in csv_output

    def test_area_chart_with_polars(self):
        """Test creating an AreaChart with Polars DataFrame."""
        from datawrapper.charts import AreaChart

        # Create a Polars DataFrame
        df = pl.DataFrame(
            {"Date": ["2023-01", "2023-02", "2023-03"], "Value": [10, 20, 15]}
        )

        # Create a chart with Polars data
        chart = AreaChart(
            title="Area Chart Example",
            data=df,
        )

        # Verify the chart was created
        assert chart.title == "Area Chart Example"
        assert chart.data is not None

        # Verify serialization works
        csv_output = chart.serialize_data()
        assert csv_output is not None
        assert "Date,Value" in csv_output

    def test_scatter_plot_with_polars(self):
        """Test creating a ScatterPlot with Polars DataFrame."""
        from datawrapper.charts import ScatterPlot

        # Create a Polars DataFrame
        df = pl.DataFrame({"X": [1, 2, 3, 4, 5], "Y": [2, 4, 6, 8, 10]})

        # Create a chart with Polars data
        chart = ScatterPlot(
            title="Scatter Plot Example",
            data=df,
        )

        # Verify the chart was created
        assert chart.title == "Scatter Plot Example"
        assert chart.data is not None

        # Verify serialization works
        csv_output = chart.serialize_data()
        assert csv_output is not None
        assert "X,Y" in csv_output

    def test_empty_polars_dataframe(self):
        """Test that empty Polars DataFrames are handled correctly."""
        from datawrapper.charts import BarChart

        # Create an empty Polars DataFrame
        df = pl.DataFrame({"A": [], "B": []})

        # Create a chart with empty data
        chart = BarChart(
            title="Empty Chart",
            data=df,
        )

        # Verify serialization returns None for empty data
        csv_output = chart.serialize_data()
        assert csv_output is None

    def test_mixed_dataframe_types(self):
        """Test that we can work with both pandas and Polars in the same session."""
        import pandas as pd

        from datawrapper.charts import BarChart

        # Create a pandas DataFrame
        df_pandas = pd.DataFrame({"A": [1, 2], "B": [3, 4]})

        # Create a Polars DataFrame
        df_polars = pl.DataFrame({"A": [1, 2], "B": [3, 4]})

        # Create charts with both types
        chart_pandas = BarChart(title="Pandas Chart", data=df_pandas)
        chart_polars = BarChart(title="Polars Chart", data=df_polars)

        # Both should serialize correctly
        csv_pandas = chart_pandas.serialize_data()
        csv_polars = chart_polars.serialize_data()

        assert csv_pandas is not None
        assert csv_polars is not None
        # The CSV output should be the same
        assert "A,B" in csv_pandas
        assert "A,B" in csv_polars


@pytest.mark.skipif(not HAS_POLARS, reason="Polars not installed")
class TestDataFrameUtilities:
    """Test the dataframe utility functions with Polars."""

    def test_to_csv_with_polars(self):
        """Test to_csv utility with Polars DataFrame."""
        from datawrapper.dataframe_utils import to_csv

        df = pl.DataFrame({"A": [1, 2], "B": [3, 4]})
        csv_output = to_csv(df)

        assert csv_output is not None
        assert "A,B" in csv_output
        assert "1,3" in csv_output

    def test_is_empty_with_polars(self):
        """Test is_empty utility with Polars DataFrame."""
        from datawrapper.dataframe_utils import is_empty

        # Non-empty dataframe
        df = pl.DataFrame({"A": [1, 2]})
        assert not is_empty(df)

        # Empty dataframe
        df_empty = pl.DataFrame({"A": []})
        assert is_empty(df_empty)

    def test_from_csv_with_polars_output(self):
        """Test from_csv utility returns pandas (for compatibility)."""
        import pandas as pd

        from datawrapper.dataframe_utils import from_csv

        # Test with CSV string
        csv_str = "A,B\n1,3\n2,4"
        df = from_csv(csv_str)

        # Should return pandas DataFrame for backward compatibility
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ["A", "B"]
        assert len(df) == 2

    def test_from_csv_with_polars_input(self):
        """Test from_csv utility can accept Polars DataFrame."""
        import pandas as pd

        from datawrapper.dataframe_utils import from_csv

        # Test with Polars DataFrame input
        df_polars = pl.DataFrame({"A": [1, 2], "B": [3, 4]})
        df = from_csv(df_polars)

        # Should convert to pandas DataFrame
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ["A", "B"]
        assert len(df) == 2
