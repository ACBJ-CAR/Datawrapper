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
        alias="symbol-shape",
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

    #: Column name for latitude coordinates
    lat: str | None = Field(
        default=None,
        description="Column to use for latitude coordinates",
    )

    #: Column name for longitude coordinates
    lon: str | None = Field(
        default=None,
        description="Column to use for longitude coordinates",
    )

    #: Column name for addresses/place names
    address: str | None = Field(
        default=None,
        description="Column to use for geocodable addresses/place names",
    )

    #: Column name for symbol area/size values
    area: str | None = Field(
        default=None,
        description="Column to use for area/size values",
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
        alias="symbol-opacity",
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
        alias="blend-multiply",
        description="Use multiply blend mode for overlapping symbols",
    )

    #
    # Map Settings
    #

    #: Basemap to use (e.g., 'usa', 'world', 'europe')
    basemap: str | None = Field(
        default=None,
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
        alias="map-padding",
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
        alias="legends",
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
        alias="clustering",
        description="Symbol clustering configuration",
    )

    #
    # Axes Configuration (for API serialization)
    #

    @property
    def _axes(self) -> dict[str, str]:
        """Get axes configuration for API."""
        axes: dict[str, str] = {}
        if self.lat:
            axes["lat"] = self.lat
        if self.lon:
            axes["lon"] = self.lon
        if self.address:
            axes["address"] = self.address
        if self.area:
            axes["area"] = self.area
        if self.size_by:
            axes["size"] = self.size_by
        if self.color_by:
            axes["color"] = self.color_by
        if self.label_by:
            axes["label"] = self.label_by
        return axes

    @staticmethod
    def _expand_dotted_keys(data: dict[str, Any]) -> dict[str, Any]:
        """Expand dotted keys (e.g. a.b) into nested dictionaries."""
        result: dict[str, Any] = {}
        for key, value in data.items():
            if "." not in key:
                result[key] = value
                continue

            parts = key.split(".")
            current = result
            for part in parts[:-1]:
                existing = current.get(part)
                if not isinstance(existing, dict):
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = value
        return result

    def serialize_model(self) -> dict[str, Any]:
        """Serialize symbol map model to Datawrapper API format."""
        model = super().serialize_model()

        visualize: dict[str, Any] = {}

        if self.basemap is not None:
            visualize["basemap"] = self.basemap
        if self.show_shape is not None:
            visualize["symbol-shape"] = (
                self.show_shape.value
                if isinstance(self.show_shape, SymbolMapShape)
                else self.show_shape
            )
        if self.max_size is not None:
            visualize["max-size"] = self.max_size
        if self.color_palette is not None:
            visualize["color-palette"] = self.color_palette
        if self.opacity is not None:
            visualize["symbol-opacity"] = self.opacity
        if self.outline is not None:
            visualize["outline"] = self.outline
        if self.multiply is not None:
            visualize["blend-multiply"] = self.multiply
        if self.crop_to_data is not None:
            visualize["crop-to-data"] = self.crop_to_data
        if self.padding is not None:
            visualize["map-padding"] = self.padding
        if self.hide_region_borders is not None:
            visualize["hide-region-borders"] = self.hide_region_borders
        if self.style is not None:
            visualize["style"] = (
                self.style.value if isinstance(self.style, MapStyle) else self.style
            )

        # Keep existing field for compatibility while providing a raw scale key.
        color_scale_value = (
            self.color_scale.value
            if isinstance(self.color_scale, ColorScale)
            else self.color_scale
        )
        visualize["color-scale"] = color_scale_value

        if self.legend:
            legend = (
                self.legend
                if isinstance(self.legend, dict)
                else self.legend.model_dump(by_alias=True, exclude_none=True)
            )
            visualize["legends"] = self._expand_dotted_keys(legend)

        if self.tooltip:
            tooltip = (
                self.tooltip
                if isinstance(self.tooltip, dict)
                else self.tooltip.model_dump(by_alias=True, exclude_none=True)
            )
            visualize["tooltip"] = self._expand_dotted_keys(tooltip)

        if self.grouping:
            grouping = (
                self.grouping
                if isinstance(self.grouping, dict)
                else self.grouping.model_dump(by_alias=True, exclude_none=True)
            )
            visualize["clustering"] = self._expand_dotted_keys(grouping)

        model["metadata"]["visualize"].update(visualize)

        axes = self._axes
        if axes:
            model["metadata"]["axes"] = axes

        return model

    @classmethod
    def deserialize_model(cls, api_response: dict[str, Any]) -> dict[str, Any]:
        """Parse Datawrapper API response including symbol map specific fields."""
        init_data = super().deserialize_model(api_response)

        metadata = api_response.get("metadata", {})
        visualize = metadata.get("visualize", {})
        axes = metadata.get("axes", {})

        if "basemap" in visualize:
            init_data["basemap"] = visualize["basemap"]
        if "symbol-shape" in visualize:
            init_data["show_shape"] = visualize["symbol-shape"]
        if "max-size" in visualize:
            init_data["max_size"] = visualize["max-size"]
        if "color-palette" in visualize:
            init_data["color_palette"] = visualize["color-palette"]
        if "symbol-opacity" in visualize:
            init_data["opacity"] = visualize["symbol-opacity"]
        if "outline" in visualize:
            init_data["outline"] = visualize["outline"]
        if "blend-multiply" in visualize:
            init_data["multiply"] = visualize["blend-multiply"]
        if "crop-to-data" in visualize:
            init_data["crop_to_data"] = visualize["crop-to-data"]
        if "map-padding" in visualize:
            init_data["padding"] = visualize["map-padding"]
        if "hide-region-borders" in visualize:
            init_data["hide_region_borders"] = visualize["hide-region-borders"]
        if "style" in visualize:
            init_data["style"] = visualize["style"]
        if "color-scale" in visualize:
            init_data["color_scale"] = visualize["color-scale"]

        if "legends" in visualize:
            init_data["legend"] = visualize["legends"]
        if "tooltip" in visualize:
            init_data["tooltip"] = visualize["tooltip"]
        if "clustering" in visualize:
            init_data["grouping"] = visualize["clustering"]

        if "lat" in axes:
            init_data["lat"] = axes["lat"]
        if "lon" in axes:
            init_data["lon"] = axes["lon"]
        if "address" in axes:
            init_data["address"] = axes["address"]
        if "area" in axes:
            init_data["area"] = axes["area"]
        if "size" in axes:
            init_data["size_by"] = axes["size"]
        if "color" in axes:
            init_data["color_by"] = axes["color"]
        if "label" in axes:
            init_data["label_by"] = axes["label"]

        return init_data
