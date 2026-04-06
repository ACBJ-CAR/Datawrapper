"""Pydantic models for symbol map configuration."""

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class SymbolMapLegend(BaseModel):
    """Legend configuration for symbol maps."""

    model_config = ConfigDict(use_enum_values=True)

    #: Enable/disable the size legend
    size_enabled: bool | None = Field(
        default=None,
        alias="size.enabled",
        description="Enable size legend",
    )

    #: Size legend position (bottom-right, bottom-left, top-right, top-left)
    size_position: str | None = Field(
        default=None,
        alias="size.position",
        description="Size legend position",
    )

    #: Size legend title
    size_title: str | None = Field(
        default=None,
        alias="size.title",
        description="Size legend title",
    )

    #: Enable/disable the color legend
    color_enabled: bool | None = Field(
        default=None,
        alias="color.enabled",
        description="Enable color legend",
    )

    #: Color legend position (bottom-right, bottom-left, top-right, top-left)
    color_position: str | None = Field(
        default=None,
        alias="color.position",
        description="Color legend position",
    )

    #: Color legend title
    color_title: str | None = Field(
        default=None,
        alias="color.title",
        description="Color legend title",
    )

    #: Highlight legend on hover
    color_highlight_on_hover: bool | None = Field(
        default=None,
        alias="color.highlight-on-hover",
        description="Highlight on hover in legend",
    )


class SymbolMapTooltip(BaseModel):
    """Tooltip configuration for symbol maps."""

    model_config = ConfigDict(use_enum_values=True)

    #: Enable/disable tooltips
    enabled: bool | None = Field(
        default=None,
        description="Enable tooltips",
    )

    #: Tooltip title (supports {{column}} template syntax)
    title: str | None = Field(
        default=None,
        description="Tooltip title with {{column}} placeholders",
    )

    #: Tooltip body (supports {{column}} template syntax)
    body: str | None = Field(
        default=None,
        description="Tooltip body with {{column}} placeholders",
    )

    #: Field mapping for tooltips
    fields: dict[str, str] | None = Field(
        default=None,
        description="Mapping of field names to CSV columns",
    )


class SymbolMapGrouping(BaseModel):
    """Symbol grouping/clustering configuration."""

    model_config = ConfigDict(use_enum_values=True)

    #: Enable symbol clustering for nearby points
    enabled: bool | None = Field(
        default=None,
        alias="group-nearby",
        description="Enable clustering of nearby symbols",
    )

    #: Cluster shape (circle, square, hexagon, triangle-up, triangle-down)
    style: str | None = Field(
        default=None,
        alias="group-style",
        description="Shape of clustered symbols",
    )

    #: Distance in pixels for grouping
    tolerance: int | None = Field(
        default=None,
        alias="group-tolerance",
        description="Pixel distance for grouping nearby symbols",
    )
