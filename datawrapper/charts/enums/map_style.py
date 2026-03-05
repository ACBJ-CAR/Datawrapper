"""Map style enums for locator maps."""

from enum import Enum


class MapStyle(str, Enum):
    """Available map styles for locator maps."""

    DW_LIGHT = "dw-light"
    DW_EARTH = "dw-earth"
    DW_WHITE = "dw-white"
    DW_WHITE_INVERT = "dw-white-invert"

    def __str__(self) -> str:
        return self.value
