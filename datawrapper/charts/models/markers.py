"""Pydantic models for locator map markers."""

from typing import Any, Literal

from pydantic import BaseModel, Field


class MarkerIcon(BaseModel):
    """Icon configuration for point markers."""

    #: SVG path of the marker symbol
    path: str = Field(
        description="SVG path of the marker symbol"
    )

    #: Height of the marker symbol
    height: int | float = Field(
        description="Height of the marker symbol"
    )

    #: Width of the marker symbol
    width: int | float = Field(
        description="Width of the marker symbol"
    )


class MarkerText(BaseModel):
    """Text styling for point markers."""

    #: Color of the marker text
    color: str = Field(
        default="#333333",
        description="Color of the marker text"
    )

    #: Font size of the marker text
    font_size: int = Field(
        default=14,
        alias="fontSize",
        description="Font size of the marker text"
    )

    #: Outline around the marker text
    halo: str = Field(
        default="#f2f3f0",
        description="Outline/halo color around the marker text"
    )

    class Config:
        """Pydantic config."""

        populate_by_name = True


class MarkerVisibility(BaseModel):
    """Visibility settings for markers across devices."""

    #: Marker visible on mobile devices
    mobile: bool = Field(
        default=True,
        description="Marker visible on mobile devices"
    )

    #: Marker visible on desktop devices
    desktop: bool = Field(
        default=True,
        description="Marker visible on desktop devices"
    )


class MarkerTooltip(BaseModel):
    """Tooltip configuration for markers."""

    #: Text that appears in tooltip on hover
    text: str = Field(
        description="Text that appears when hovering over the marker"
    )


class PointMarker(BaseModel):
    """Point marker for locator maps.

    Point markers represent specific locations on the map with custom icons and labels.
    """

    #: Marker type
    type: Literal["point"] = Field(
        default="point",
        description="Marker type"
    )

    #: Marker text (displayed next to symbol, supports HTML)
    title: str | None = Field(
        default=None,
        description="Marker text displayed next to the symbol (supports HTML like <strong>, <br>)"
    )

    #: Icon configuration (SVG path, dimensions)
    icon: MarkerIcon | dict[str, Any] = Field(
        description="Icon configuration with SVG path and dimensions"
    )

    #: Size multiplier for the marker symbol
    scale: float = Field(
        default=1.0,
        description="Size multiplier for the marker symbol"
    )

    #: Color of the marker symbol
    marker_color: str = Field(
        default="#cc0000",
        alias="markerColor",
        description="Color of the marker symbol"
    )

    #: Position of marker text relative to symbol
    anchor: Literal[
        "bottom-left", "bottom-center", "bottom-right",
        "middle-left", "middle-center", "middle-right",
        "top-left", "top-center", "top-right"
    ] = Field(
        default="bottom-right",
        description="Position of marker text relative to symbol"
    )

    #: Vertical distance between text and symbol
    offset_y: int = Field(
        default=0,
        alias="offsetY",
        description="Vertical offset between text and symbol (can be negative)"
    )

    #: Horizontal distance between text and symbol
    offset_x: int = Field(
        default=0,
        alias="offsetX",
        description="Horizontal offset between text and symbol (can be negative)"
    )

    #: Text styling configuration
    text: MarkerText | dict[str, Any] = Field(
        default_factory=MarkerText,
        description="Text styling configuration"
    )

    #: Rotation of marker text in degrees
    rotate: int = Field(
        default=0,
        description="Rotation of marker text in degrees"
    )

    #: Whether the marker is visible
    visible: bool = Field(
        default=True,
        description="Whether the marker is visible"
    )

    #: Device-specific visibility
    visibility: MarkerVisibility | dict[str, Any] = Field(
        default_factory=MarkerVisibility,
        description="Device-specific visibility settings"
    )

    #: Marker coordinates [longitude, latitude]
    coordinates: list[float] = Field(
        description="Marker coordinates as [longitude, latitude]"
    )

    #: Tooltip configuration
    tooltip: MarkerTooltip | dict[str, Any] | None = Field(
        default=None,
        description="Tooltip that appears on hover"
    )

    #: Optional marker ID
    id: str | None = Field(
        default=None,
        description="Optional unique identifier for the marker"
    )

    class Config:
        """Pydantic config."""

        populate_by_name = True


class AreaProperties(BaseModel):
    """Styling properties for area markers."""

    #: Fill color
    fill: str = Field(
        default="#15607a",
        description="Fill color for the area"
    )

    #: Fill opacity (0-1)
    fill_opacity: float = Field(
        default=0.2,
        alias="fill-opacity",
        description="Fill opacity (0-1)"
    )

    #: Stroke color
    stroke: str = Field(
        default="#15607a",
        description="Stroke/border color"
    )

    #: Stroke width in pixels
    stroke_width: int = Field(
        default=1,
        alias="stroke-width",
        description="Stroke width in pixels"
    )

    #: Stroke opacity (0-1)
    stroke_opacity: float = Field(
        default=1.0,
        alias="stroke-opacity",
        description="Stroke opacity (0-1)"
    )

    #: Stroke dash pattern
    stroke_dasharray: str = Field(
        default="100000",
        alias="stroke-dasharray",
        description="Stroke dash pattern (e.g., '5,5' for dashed)"
    )

    #: Pattern type
    pattern: str = Field(
        default="solid",
        description="Fill pattern type"
    )

    #: Pattern line width
    pattern_line_width: int = Field(
        default=2,
        alias="pattern-line-width",
        description="Pattern line width"
    )

    #: Pattern line gap
    pattern_line_gap: int = Field(
        default=2,
        alias="pattern-line-gap",
        description="Gap between pattern lines"
    )

    class Config:
        """Pydantic config."""

        populate_by_name = True


class GeoJSONGeometry(BaseModel):
    """GeoJSON geometry object."""

    #: Geometry type
    type: str = Field(
        description="GeoJSON geometry type (e.g., 'MultiPolygon', 'LineString')"
    )

    #: Coordinates array
    coordinates: list[Any] = Field(
        description="Coordinate arrays (structure varies by geometry type)"
    )


class GeoJSONFeature(BaseModel):
    """GeoJSON feature object."""

    #: Feature type
    type: Literal["Feature"] = Field(
        default="Feature",
        description="GeoJSON feature type"
    )

    #: Feature properties
    properties: list[Any] | dict[str, Any] = Field(
        default_factory=list,
        description="Feature properties"
    )

    #: Feature geometry
    geometry: GeoJSONGeometry | dict[str, Any] = Field(
        description="GeoJSON geometry object"
    )


class AreaMarker(BaseModel):
    """Area marker for locator maps.

    Area markers represent polygonal regions on the map with custom styling.
    """

    #: Marker type
    type: Literal["area"] = Field(
        default="area",
        description="Marker type"
    )

    #: Whether the marker is visible
    visible: bool = Field(
        default=True,
        description="Whether the marker is visible"
    )

    #: Device-specific visibility
    visibility: MarkerVisibility | dict[str, Any] | None = Field(
        default=None,
        description="Device-specific visibility settings"
    )

    #: Display exact shape without simplification
    exact_shape: bool = Field(
        default=True,
        alias="exactShape",
        description="Display exact shape without simplification"
    )

    #: Display area with fill color
    fill: bool = Field(
        default=True,
        description="Display area with fill color"
    )

    #: Display area with stroke/border
    stroke: bool = Field(
        default=True,
        description="Display area with stroke/border"
    )

    #: Area styling properties
    properties: AreaProperties | dict[str, Any] = Field(
        default_factory=AreaProperties,
        description="Area styling properties"
    )

    #: GeoJSON feature with geometry
    feature: GeoJSONFeature | dict[str, Any] = Field(
        description="GeoJSON feature containing the area geometry"
    )

    #: Optional marker ID
    id: str | None = Field(
        default=None,
        description="Optional unique identifier for the marker"
    )

    class Config:
        """Pydantic config."""

        populate_by_name = True


class LineProperties(BaseModel):
    """Styling properties for line markers."""

    #: Stroke color
    stroke: str = Field(
        default="#fa8c00",
        description="Line color"
    )

    #: Stroke width in pixels
    stroke_width: int = Field(
        default=3,
        alias="stroke-width",
        description="Line width in pixels"
    )

    #: Stroke opacity (0-1)
    stroke_opacity: float = Field(
        default=1.0,
        alias="stroke-opacity",
        description="Line opacity (0-1)"
    )

    #: Stroke dash pattern
    stroke_dasharray: str = Field(
        default="100000",
        alias="stroke-dasharray",
        description="Stroke dash pattern (e.g., '5,5' for dashed)"
    )

    class Config:
        """Pydantic config."""

        populate_by_name = True


class LineMarker(BaseModel):
    """Line marker for locator maps.

    Line markers connect multiple coordinates with a visible path.
    """

    #: Marker type
    type: Literal["line"] = Field(
        default="line",
        description="Marker type"
    )

    #: Marker title/label
    title: str | None = Field(
        default=None,
        description="Marker title/label"
    )

    #: Whether the marker is visible
    visible: bool = Field(
        default=True,
        description="Whether the marker is visible"
    )

    #: Device-specific visibility
    visibility: MarkerVisibility | dict[str, Any] | None = Field(
        default=None,
        description="Device-specific visibility settings"
    )

    #: Line styling properties
    properties: LineProperties | dict[str, Any] = Field(
        default_factory=LineProperties,
        description="Line styling properties"
    )

    #: GeoJSON feature with line geometry
    feature: GeoJSONFeature | dict[str, Any] = Field(
        description="GeoJSON feature containing the line geometry (LineString)"
    )

    #: Optional marker ID
    id: str | None = Field(
        default=None,
        description="Optional unique identifier for the marker"
    )

    class Config:
        """Pydantic config."""

        populate_by_name = True
