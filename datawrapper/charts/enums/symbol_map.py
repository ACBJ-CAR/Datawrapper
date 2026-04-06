"""Enums for symbol map configuration."""

from enum import Enum


class SymbolMapShape(str, Enum):
    """Shape options for symbols on symbol maps.

    Controls the shape of point symbols displayed on symbol maps.

    Attributes:
        CIRCLE: Circular symbols
        SQUARE: Square symbols
        DIAMOND: Diamond-shaped symbols
        HEXAGON: Hexagonal symbols
        TRIANGLE_UP: Upward-pointing triangular symbols
        TRIANGLE_DOWN: Downward-pointing triangular symbols
        MARKER: Map marker/pin symbols

    Examples:
        >>> from datawrapper.charts import SymbolMap, SymbolMapShape
        >>> chart = SymbolMap(
        ...     title="City Locations",
        ...     data=df,
        ...     show_shape=SymbolMapShape.CIRCLE,
        ... )
    """

    CIRCLE = "circle"
    SQUARE = "square"
    DIAMOND = "diamond"
    HEXAGON = "hexagon"
    TRIANGLE_UP = "triangle-up"
    TRIANGLE_DOWN = "triangle-down"
    MARKER = "marker"


class ColorScale(str, Enum):
    """Color scale options for symbol maps.

    Controls how color values are mapped to the color palette.

    Attributes:
        LINEAR: Linear color scale
        LOG: Logarithmic color scale (for skewed data)
        CATEGORICAL: Discrete/categorical color scale

    Examples:
        >>> from datawrapper.charts import SymbolMap, ColorScale
        >>> chart = SymbolMap(
        ...     title="Population",
        ...     data=df,
        ...     color_scale=ColorScale.LOG,
        ... )
    """

    LINEAR = "linear"
    LOG = "log"
    CATEGORICAL = "categorical"
