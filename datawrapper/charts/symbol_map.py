"""Datawrapper Symbol Map chart class."""

from typing import Any, Literal

from pydantic import ConfigDict, Field, field_validator

from datawrapper.charts.enums.symbol_map import ColorScale, SymbolMapShape
from datawrapper.charts.models.symbol_map import (
    SymbolMapGrouping,
    SymbolMapLegend,
    SymbolMapTooltip,
)

from .base import BaseChart
from .enums.map_style import MapStyle


class SymbolMap(BaseChart):
    """A Datawrapper symbol map for displaying data-driven point symbols on a map.

    Symbol maps show data about specific point locations using geometric shapes that can be
    sized and colored based on data values. They're ideal for visualizing geographic point
    data where both the location and additional attributes are important.

    Symbol maps require either:
    - CSV data with 'lat' and 'long' columns (recommended for accuracy)
    - CSV data with place names/addresses that Datawrapper will geocode

    Plus at least one numeric column for sizing/coloring the symbols.

    Example:
        >>> from datawrapper.charts import SymbolMap
        >>> from datawrapper.charts.enums.symbol_map import SymbolMapShape, ColorScale
        >>> import pandas as pd
        >>>
        >>> # Create data with lat/long coordinates
        >>> data = pd.DataFrame({
        ...     'lat': [40.6635, 42.383, 41.8376],
        ...     'long': [-73.9387, -83.1022, -87.6818],
        ...     'city': ['New York', 'Detroit', 'Chicago'],
        ...     'population': [8537673, 672795, 2704958],
        ...     'change_pct': [4.43, -5.74, 0.35]
        ... })
        >>>
        >>> chart = SymbolMap(
        ...     title="US Cities Population",
        ...     data=data,
        ...     show_shape=SymbolMapShape.CIRCLE,
        ...     size_by="population",
        ...     color_by="change_pct",
        ...     color_scale=ColorScale.LINEAR,
        ... )
        >>> chart.create().publish()
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
                    "chart-type": "d3-maps-symbols",
                    "title": "City Locations",
                    "source_name": "My Data Source",
                }
            ]
        },
    )

    #: The type of datawrapper chart to create
    chart_type: Literal["d3-maps-symbols"] = Field(
        default="d3-maps-symbols",
        alias="chart-type",
        description="The type of datawrapper chart to create",
    )

    #
    # Symbol Display
    #

    #: The shape of symbols (circle, square, diamond, hexagon, triangle-up, triangle-down, marker)
    show_shape: SymbolMapShape | str = Field(
        default=SymbolMapShape.CIRCLE,
        alias="shape",
        description="Shape of symbols on the map",
    )

    @field_validator("show_shape", mode="before")
    @classmethod
    def validate_shape(cls, v: Any) -> str:
        """Validate shape is a valid SymbolMapShape."""
        if isinstance(v, SymbolMapShape):
            return v.value
        if isinstance(v, str):
            if v in [s.value for s in SymbolMapShape]:
                return v
            raise ValueError(f"Invalid shape: {v}")
        raise ValueError("shape must be a SymbolMapShape enum or string")

    #
    # Data Mapping
    #

    #: Column name or "--" for the size of symbols
    size_by: str | None = Field(
        default=None,
        alias="size-by",
        description="Column to use for symbol size (or '--' for uniform size)",
    )

    #: Column name for the color of symbols
    color_by: str | None = Field(
        default=None,
        alias="color-by",
        description="Column to use for symbol color",
    )

    #: Column name for symbol labels/names
    label_by: str | None = Field(
        default=None,
        alias="label-by",
        description="Column to use for symbol labels",
    )

    #
    # Symbol Sizing
    #

    #: Maximum symbol size
    max_size: int | None = Field(
        default=None,
        alias="max-size",
        description="Maximum symbol size (responsive on mobile)",
    )

    #
    # Color Configuration
    #

    #: Color scale type (linear, log, categorical)
    color_scale: ColorScale | str = Field(
        default=ColorScale.LINEAR,
        alias="color-scale",
        description="How to map color values (linear, log, categorical)",
    )

    @field_validator("color_scale", mode="before")
    @classmethod
    def validate_color_scale(cls, v: Any) -> str:
        """Validate color_scale is a valid ColorScale."""
        if isinstance(v, ColorScale):
            return v.value
        if isinstance(v, str):
            if v in [s.value for s in ColorScale]:
                return v
            raise ValueError(f"Invalid color scale: {v}")
        raise ValueError("color_scale must be a ColorScale enum or string")

    #: Color palette name
    color_palette: str | None = Field(
        default=None,
        alias="color-palette",
        description="Color palette name (e.g., 'warm', 'cool', 'RdBu')",
    )

    #: Symbol transparency/opacity (0-1)
    opacity: float | None = Field(
        default=None,
        description="Symbol opacity/transparency (0-1)",
    )

    #: Show symbol outlines
    outline: bool | None = Field(
        default=None,
        description="Show outlines on symbols",
    )

    #: Use multiply blend mode for overlapping symbols
    multiply: bool | None = Field(
        default=None,
        description="Use multiply blend mode for overlapping symbols",
    )

    #
    # Map Settings
    #

    #: Basemap to use (e.g., 'usa', 'world', 'europe')
    basemap: str = Field(
        description="Basemap to display (e.g., 'usa', 'world', 'europe')",
    )

    #: Crop map to data extent
    crop_to_data: bool | None = Field(
        default=None,
        alias="crop-to-data",
        description="Crop the map to the geographic extent of the data",
    )

    #: Padding around data as percentage
    padding: int | None = Field(
        default=None,
        description="Percentage padding around data extent",
    )

    #: Hide region/administrative boundaries
    hide_region_borders: bool | None = Field(
        default=None,
        alias="hide-region-borders",
        description="Hide administrative region boundaries",
    )

    #: Map style/theme
    style: MapStyle | str = Field(
        default=MapStyle.DW_LIGHT,
        description="Map base style (dw-light, dw-earth, dw-white, dw-white-invert)",
    )

    #
    # Legend and Tooltips
    #

    #: Legend configuration
    legend: SymbolMapLegend | dict[str, Any] | None = Field(
        default=None,
        description="Legend configuration",
    )

    #: Tooltip configuration
    tooltip: SymbolMapTooltip | dict[str, Any] | None = Field(
        default=None,
        description="Tooltip configuration",
    )

    #
    # Grouping/Clustering
    #

    #: Symbol grouping/clustering configuration
    grouping: SymbolMapGrouping | dict[str, Any] | None = Field(
        default=None,
        description="Symbol clustering configuration",
    )

    #
    # Axes Configuration (for API serialization)
    #

    @property
    def _axes(self) -> dict[str, str]:
        """Get axes configuration for API."""
        axes = {}
        if self.size_by:
            axes["size"] = self.size_by
        if self.color_by:
            axes["color"] = self.color_by
        if self.label_by:
            axes["label"] = self.label_by
        return axes
