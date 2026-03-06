"""Datawrapper Locator Map chart class."""

import json
from typing import Any, Literal

from pydantic import ConfigDict, Field, field_validator, model_validator

from datawrapper.charts.models.locator_map import (
    MapKey,
    MapView,
    MapVisibility,
    MiniMap,
)
from datawrapper.charts.models.markers import AreaMarker, LineMarker, PointMarker

from .base import BaseChart
from .enums.map_style import MapStyle


class LocatorMap(BaseChart):
    """A Datawrapper locator map for displaying locations on a geographic map.

    Locator maps are used to highlight and locate specific points, areas, or routes
    on a map. Unlike other charts, locator maps use markers (point, area, line) instead
    of tabular data.

    Example:
        >>> from datawrapper.charts import LocatorMap
        >>> from datawrapper.charts.models.locator_map import MapView
        >>> from datawrapper.charts.models.markers import PointMarker, MarkerIcon
        >>>
        >>> # Create a locator map with a point marker
        >>> point = PointMarker(
        ...     title="Buckingham Palace",
        ...     icon=MarkerIcon(
        ...         path="M1000 350a500 500 0 0 0-500-500...",
        ...         height=700,
        ...         width=1000
        ...     ),
        ...     coordinates=[-0.140634, 51.501476]
        ... )
        >>>
        >>> chart = LocatorMap(
        ...     title="Locations in London",
        ...     markers=[point],
        ...     view=MapView(center=[-0.106, 51.523], zoom=8),
        ...     style=MapStyle.DW_LIGHT,
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
                    "chart-type": "locator-map",
                    "title": "Key Locations",
                    "source_name": "My Data Source",
                }
            ]
        },
    )

    #: The type of datawrapper chart to create
    chart_type: Literal["locator-map"] = Field(
        default="locator-map",
        alias="chart-type",
        description="The type of datawrapper chart to create",
    )

    #
    # Markers (replaces standard data field)
    #

    #: List of markers to display on the map (point, area, or line markers)
    markers: list[PointMarker | AreaMarker | LineMarker | dict[str, Any]] = Field(
        default_factory=list,
        description="List of markers (point, area, or line) to display on the map",
    )

    @field_validator("markers", mode="before")
    @classmethod
    def validate_markers(cls, v: Any) -> list:
        """Validate that markers is a list."""
        if v is None:
            return []
        if not isinstance(v, list):
            raise ValueError("markers must be a list of marker objects or dicts")
        return v

    @model_validator(mode="after")
    def validate_no_dataframe(self) -> "LocatorMap":
        """Ensure data field is not set for locator maps.

        Locator maps use markers, not tabular data.
        """
        # Check if data attribute exists and is not empty
        if hasattr(self, "data"):
            data_value = self.data
            # Check if data is a non-empty DataFrame or non-empty list
            if data_value is not None:
                try:
                    import pandas as pd
                    if isinstance(data_value, pd.DataFrame) and not data_value.empty:
                        raise ValueError(
                            "LocatorMap does not accept DataFrame data. "
                            "Use the 'markers' field with PointMarker, AreaMarker, or LineMarker objects instead."
                        )
                except ImportError:
                    pass

                if isinstance(data_value, list) and len(data_value) > 0:
                    raise ValueError(
                        "LocatorMap does not accept list data. "
                        "Use the 'markers' field with PointMarker, AreaMarker, or LineMarker objects instead."
                    )

        return self

    #
    # View settings
    #

    #: Map view configuration (center, zoom, borders, aspect ratio, rotation, tilt)
    view: MapView | dict[str, Any] = Field(
        default_factory=MapView,
        description="Map view configuration with center, zoom, fit, height, bearing, pitch",
    )

    #
    # Map style and settings
    #

    #: Map base style/theme
    style: MapStyle | str = Field(
        default=MapStyle.DW_LIGHT,
        description="Map base style (dw-light, dw-earth, dw-white, dw-white-invert)",
    )

    #: Enable/disable map labels
    map_label: bool | None = Field(
        default=None,
        alias="map-label",
        description="Enable/disable map labels",
    )

    #: Show compass control
    compass: bool | None = Field(
        default=None,
        description="Show compass control",
    )

    #: Show scale control
    scale: bool | None = Field(
        default=None,
        description="Show scale control",
    )

    #: Default map size in editor (doesn't affect published size)
    default_map_size: int | None = Field(
        default=None,
        alias="default-map-size",
        description="Default map size in editor (doesn't affect published map)",
    )

    #
    # Layer visibility
    #

    #: Layer visibility settings (boundaries, buildings, vegetation, etc.)
    visibility: MapVisibility | dict[str, Any] | None = Field(
        default=None,
        description="Layer visibility settings for map layers",
    )

    #
    # Additional features
    #

    #: Mini map configuration
    mini_map: MiniMap | dict[str, Any] | None = Field(
        default=None,
        alias="mini-map",
        description="Mini map configuration (enabled, bounds)",
    )

    #: Map key/legend configuration
    key: MapKey | dict[str, Any] | None = Field(
        default=None,
        description="Map key/legend configuration (enabled, title, items)",
    )

    def serialize_data(self) -> str:
        """Serialize markers to JSON format for the Datawrapper API.

        Locator maps require markers in JSON format, not CSV like other charts.

        Returns:
            JSON string containing markers data
        """
        if not self.markers:
            return json.dumps({"markers": []})

        serialized_markers = []
        for marker in self.markers:
            if isinstance(marker, dict):
                # Already a dict, use as-is
                serialized_markers.append(marker)
            else:
                # Pydantic model, convert to dict using model_dump with by_alias=True
                serialized_markers.append(marker.model_dump(by_alias=True, exclude_none=True))

        return json.dumps({"markers": serialized_markers})

    @classmethod
    def deserialize_data(cls, data_response: dict[str, Any] | str) -> Any:
        """Deserialize marker data from the Datawrapper API response.

        Locator maps store markers as JSON, not CSV like other charts.
        This method validates the marker data structure but returns an empty
        DataFrame since LocatorMap uses markers, not tabular data.

        Args:
            data_response: The data response from the API (dict with markers or JSON string)

        Returns:
            Empty DataFrame (LocatorMap doesn't use the data field)
        """
        import pandas as pd

        # Locator maps don't use tabular data, so return empty DataFrame
        # The actual marker data is handled separately via get() method
        return pd.DataFrame()

    def serialize_model(self) -> dict:
        """Serialize the locator map model to API format.

        Returns:
            Dictionary containing the serialized chart metadata compatible with
            the Datawrapper API
        """
        # Call parent class's serialize_model method
        model = super().serialize_model()

        # Build visualize section with locator map specific properties
        visualize = {}

        # Add view settings
        if isinstance(self.view, dict):
            view_dict = self.view
        elif self.view:
            view_dict = self.view.model_dump(exclude_none=True)
        else:
            view_dict = {}

        if view_dict:
            visualize["view"] = view_dict

        # Add style
        style_value = self.style.value if isinstance(self.style, MapStyle) else self.style
        visualize["style"] = style_value

        # Add optional settings
        if self.map_label is not None:
            visualize["mapLabel"] = self.map_label
        if self.compass is not None:
            visualize["compass"] = self.compass
        if self.scale is not None:
            visualize["scale"] = self.scale
        if self.default_map_size is not None:
            visualize["defaultMapSize"] = self.default_map_size

        # Add visibility settings
        if self.visibility:
            if isinstance(self.visibility, dict):
                visibility_dict = self.visibility
            else:
                visibility_dict = self.visibility.model_dump(exclude_none=True)

            if visibility_dict:
                visualize["visibility"] = visibility_dict

        # Add mini map
        if self.mini_map:
            if isinstance(self.mini_map, dict):
                mini_map_dict = self.mini_map
            else:
                mini_map_dict = self.mini_map.model_dump(exclude_none=True)

            if mini_map_dict:
                visualize["miniMap"] = mini_map_dict

        # Add key/legend
        if self.key:
            if isinstance(self.key, dict):
                key_dict = self.key
            else:
                key_dict = self.key.model_dump(exclude_none=True)

            if key_dict:
                visualize["key"] = key_dict

        # Update the metadata visualize section
        model["metadata"]["visualize"].update(visualize)

        return model

    @classmethod
    def deserialize_model(cls, api_response: dict[str, Any]) -> dict[str, Any]:
        """Parse Datawrapper API response including locator map specific fields.

        Args:
            api_response: The JSON response from the chart metadata endpoint

        Returns:
            Dictionary that can be used to initialize the LocatorMap model
        """
        # Call parent to get base fields
        init_data = super().deserialize_model(api_response)

        # Extract locator-map-specific sections
        metadata = api_response.get("metadata", {})
        visualize = metadata.get("visualize", {})

        # Parse view settings
        if "view" in visualize:
            init_data["view"] = MapView(**visualize["view"])

        # Parse style
        if "style" in visualize:
            init_data["style"] = visualize["style"]

        # Parse optional settings
        if "mapLabel" in visualize:
            init_data["map_label"] = visualize["mapLabel"]
        if "compass" in visualize:
            init_data["compass"] = visualize["compass"]
        if "scale" in visualize:
            init_data["scale"] = visualize["scale"]
        if "defaultMapSize" in visualize:
            init_data["default_map_size"] = visualize["defaultMapSize"]

        # Parse visibility settings
        if "visibility" in visualize:
            init_data["visibility"] = MapVisibility(**visualize["visibility"])

        # Parse mini map
        if "miniMap" in visualize:
            init_data["mini_map"] = MiniMap(**visualize["miniMap"])

        # Parse key/legend
        if "key" in visualize:
            init_data["key"] = MapKey(**visualize["key"])

        # Note: Markers are stored separately in the data endpoint, not in metadata
        # They will be empty by default and must be fetched/set separately
        init_data["markers"] = []

        return init_data

        @classmethod
        def get(cls, chart_id: str, access_token: str | None = None) -> "LocatorMap":
            """Fetch a locator map from the Datawrapper API.

            Overrides the base class method to properly handle marker data.

            Args:
                chart_id: The ID of the chart to fetch
                access_token: Optional API access token

            Returns:
                LocatorMap instance with all data populated from the API
            """
            import requests
            from datawrapper.exceptions import FailedRequestError, RateLimitError

            # Get chart instance using parent class method
            instance = super().get(chart_id, access_token)

            # Fetch marker data from the data endpoint
            if instance._client:
                try:
                    # Construct data endpoint URL
                    url = f"{instance._client.api_url}/v3/charts/{chart_id}/data"
                    headers = {
                        "Authorization": f"Bearer {instance._client.access_token}",
                        "Accept": "application/json",
                    }

                    response = requests.get(url, headers=headers, timeout=30)

                    if response.status_code == 200:
                        # Extract marker data
                        marker_data = response.json()
                        if isinstance(marker_data, dict) and "markers" in marker_data:
                            markers_list = marker_data.get("markers", [])
                            if isinstance(markers_list, list):
                                instance.markers = markers_list
                    elif response.status_code == 429:
                        raise RateLimitError(response.text)
                    elif response.status_code >= 400:
                        raise FailedRequestError(response.text)
                except requests.RequestException as e:
                    # If marker fetch fails, just continue with empty markers
                    pass

            return instance
