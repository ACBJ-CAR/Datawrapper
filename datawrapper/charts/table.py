"""Table visualization class for Datawrapper API."""

from typing import Any, Literal

import pandas as pd
from pydantic import ConfigDict, Field

from .base import BaseChart
from .models import ColumnFormat


class Table(BaseChart):
    """A Datawrapper table visualization for displaying tabular data.

    Tables are useful for displaying detailed data in a structured format with
    support for column formatting, ordering, and visibility configuration.

    Example:
        >>> import pandas as pd
        >>> from datawrapper.charts import Table
        >>> 
        >>> df = pd.DataFrame({
        ...     "Country": ["USA", "China", "India"],
        ...     "Population": [331000000, 1412000000, 1380000000],
        ...     "GDP": [22.94, 17.73, 3.29]
        ... })
        >>> 
        >>> # Create and configure a table
        >>> table = Table(
        ...     title="Countries by Population and GDP",
        ...     data=df,
        ...     source_name="World Bank",
        ...     byline="Data Team"
        ... )
        >>> 
        >>> # Create the table in Datawrapper
        >>> table.create()
        >>> 
        >>> # Update configuration and publish
        >>> table.title = "Updated Title"
        >>> table.update().publish()
    """

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        validate_assignment=True,
        validate_default=True,
        use_enum_values=True,
        json_schema_extra={
            "examples": [
                {
                    "chart-type": "tables",
                    "title": "Sales Data by Region",
                    "source_name": "Sales Database",
                    "data": pd.DataFrame(
                        {
                            "Region": ["North", "South", "East", "West"],
                            "Q1": [100, 150, 200, 120],
                            "Q2": [110, 160, 210, 130],
                            "Q3": [120, 170, 220, 140],
                        }
                    ),
                    "column_order": [0, 1, 2, 3],
                    "column_formats": [
                        {"column": "Region", "type": "text"},
                        {"column": "Q1", "type": "number", "number-format": "n0"},
                        {"column": "Q2", "type": "number", "number-format": "n0"},
                        {"column": "Q3", "type": "number", "number-format": "n0"},
                    ],
                }
            ]
        },
    )

    #: The type of datawrapper visualization
    chart_type: Literal["tables"] = Field(
        default="tables",
        alias="chart-type",
        description="The type of datawrapper visualization (always 'tables' for Table)",
    )

    #
    # Table Configuration
    #

    #: The order of columns as indices (0-based). If provided, columns will be displayed in this order.
    column_order: list[int] = Field(
        default_factory=list,
        alias="column-order",
        description="The order of columns as indices. If empty, columns will display in their original order.",
    )

    #: List of column format specifications for controlling number formatting, alignment, etc.
    column_formats: list[dict[str, Any] | ColumnFormat] = Field(
        default_factory=list,
        alias="column-formats",
        description="List of column format specifications to control number formatting, alignment, and other column-specific settings.",
    )

    def serialize_model(self) -> dict[str, Any]:
        """Serialize the table model to Datawrapper API format.

        Returns:
            Dictionary with the table configuration in API format.
        """
        # Call the parent class's serialize_model method
        model = super().serialize_model()

        # Get the data section with transformations
        data_section = model["metadata"]["data"].copy()

        # Add table-specific fields to data section
        if self.column_order:
            data_section["column-order"] = self.column_order

        # Serialize column formats
        if self.column_formats:
            column_format_dict = {}
            for col_format in self.column_formats:
                if isinstance(col_format, dict):
                    # Convert dict to ColumnFormat if needed for validation
                    col_fmt = ColumnFormat.model_validate(col_format)
                    column_name = col_fmt.column
                    column_format_dict[column_name] = col_fmt.model_dump(
                        by_alias=True, exclude={"column"}
                    )
                else:
                    # Already a ColumnFormat object
                    column_name = col_format.column
                    column_format_dict[column_name] = col_format.model_dump(
                        by_alias=True, exclude={"column"}
                    )
            if column_format_dict:
                data_section["column-format"] = column_format_dict

        # Update the data section in metadata
        model["metadata"]["data"] = data_section

        return model

    @classmethod
    def deserialize_model(cls, api_response: dict[str, Any]) -> dict[str, Any]:
        """Parse Datawrapper API response for table-specific fields.

        Args:
            api_response: The JSON response from the chart metadata endpoint

        Returns:
            Dictionary that can be used to initialize the Table model
        """
        # Call parent to get base fields
        init_data = super().deserialize_model(api_response)

        # Extract table-specific sections
        metadata = api_response.get("metadata", {})
        data_section = metadata.get("data", {})

        # Extract column order
        if "column-order" in data_section:
            init_data["column_order"] = data_section["column-order"]

        # Extract column formats
        if "column-format" in data_section:
            col_fmt_dict = data_section["column-format"]
            column_formats = []
            for column_name, format_config in col_fmt_dict.items():
                # Create a ColumnFormat with the column name included
                format_with_column = {"column": column_name, **format_config}
                column_formats.append(format_with_column)
            if column_formats:
                init_data["column_formats"] = column_formats

        return init_data
