"""Pydantic models for locator map configuration."""

from typing import Any

from pydantic import BaseModel, Field


class MapView(BaseModel):
    """Map view configuration (center, zoom, fit, bearing, pitch, height)."""

    #: Map center as [longitude, latitude]
    center: list[float] | None = Field(
        default=None,
        description="Map center coordinates as [longitude, latitude]",
    )

    #: Zoom level (0-15, where 0 is whole world)
    zoom: int | None = Field(
        default=None,
        description="Zoom level (0-15, where 0 = whole world)",
    )

    #: Fit bounds [top, right, bottom, left] as coordinate pairs
    fit: dict[str, list[float]] | None = Field(
        default=None,
        description="Fit bounds with keys 'top', 'right', 'bottom', 'left' containing [lon, lat] coordinate pairs",
    )

    #: Map aspect ratio in percentage (100 = square)
    height: int | None = Field(
        default=None,
        description="Aspect ratio in percentage (100 = square, 50 = landscape)",
    )

    #: Map rotation in degrees (0 = north-oriented)
    bearing: int | None = Field(
        default=None,
        description="Map rotation in degrees (0 = north-oriented)",
    )

    #: Map tilt in degrees (0-60)
    pitch: int | None = Field(
        default=None,
        description="Map tilt in degrees (0-60)",
    )

    class Config:
        """Pydantic config."""

        use_enum_values = True


class MapVisibility(BaseModel):
    """Layer visibility settings for locator maps."""

    #: Show country boundaries
    boundary_country: bool | None = Field(
        default=None,
        alias="boundary_country",
        description="Show country boundaries",
    )

    #: Show state/province boundaries
    boundary_state: bool | None = Field(
        default=None,
        alias="boundary_state",
        description="Show state/province boundaries",
    )

    #: Show buildings
    building: bool | None = Field(
        default=None,
        description="Show buildings",
    )

    #: Show vegetation/parks
    green: bool | None = Field(
        default=None,
        description="Show vegetation/parks",
    )

    #: Show mountains
    mountains: bool | None = Field(
        default=None,
        description="Show mountains",
    )

    #: Show roads
    roads: bool | None = Field(
        default=None,
        description="Show roads",
    )

    #: Show urban areas
    urban: bool | None = Field(
        default=None,
        description="Show urban areas",
    )

    #: Show water features
    water: bool | None = Field(
        default=None,
        description="Show water features",
    )

    #: Show 3D buildings
    building_3d: bool | None = Field(
        default=None,
        alias="building3d",
        description="Show 3D buildings",
    )

    class Config:
        """Pydantic config."""

        populate_by_name = True


class MiniMap(BaseModel):
    """Mini map configuration."""

    #: Enable mini map
    enabled: bool | None = Field(
        default=None,
        description="Enable mini map",
    )

    #: Bounds for mini map
    bounds: list[Any] | None = Field(
        default=None,
        description="Bounds for mini map",
    )


class MapKey(BaseModel):
    """Map key/legend configuration."""

    #: Enable map key
    enabled: bool | None = Field(
        default=None,
        description="Enable map key",
    )

    #: Title for the map key
    title: str | None = Field(
        default=None,
        description="Title for the map key",
    )

    #: Items in the map key
    items: list[dict[str, Any]] | None = Field(
        default=None,
        description="Items in the map key",
    )
