"""Unit tests for SymbolMap serialization/deserialization."""

import pandas as pd

from datawrapper.charts import SymbolMap


def test_symbol_map_serializes_fields_to_visualize_and_axes():
    """Symbol map fields should be routed to metadata.visualize and metadata.axes."""
    data = pd.DataFrame(
        {
            "LAT": [52.52],
            "LON": [13.405],
            "geo": ["Berlin"],
            "pct_change": [0.05],
        }
    )

    chart = SymbolMap(
        title="Demographic changes",
        data=data,
        basemap="europe-nuts3-2021",
        show_shape="arrow",
        max_size=35,
        opacity=1,
        multiply=False,
        hide_region_borders=True,
        lat="LAT",
        lon="LON",
        address="geo",
        area="pct_change",
    )

    model = chart.serialize_model()
    metadata = model["metadata"]

    assert metadata["visualize"]["basemap"] == "europe-nuts3-2021"
    assert metadata["visualize"]["symbol-shape"] == "arrow"
    assert metadata["visualize"]["max-size"] == 35
    assert metadata["visualize"]["symbol-opacity"] == 1
    assert metadata["visualize"]["blend-multiply"] is False
    assert metadata["visualize"]["hide-region-borders"] is True

    assert metadata["axes"]["lat"] == "LAT"
    assert metadata["axes"]["lon"] == "LON"
    assert metadata["axes"]["address"] == "geo"
    assert metadata["axes"]["area"] == "pct_change"


def test_symbol_map_deserializes_visualize_and_axes_fields():
    """Symbol map visualize and axes settings should deserialize back into model fields."""
    api_response = {
        "id": "ISquW",
        "type": "d3-maps-symbols",
        "title": "Europe's countries on different demographic paths",
        "metadata": {
            "visualize": {
                "basemap": "europe-nuts3-2021",
                "symbol-shape": "arrow",
                "max-size": 35,
                "symbol-opacity": 1,
                "blend-multiply": False,
                "hide-region-borders": True,
            },
            "axes": {
                "lat": "LAT",
                "lon": "LON",
                "area": "pct_change",
                "address": "geo",
            },
        },
    }

    init_data = SymbolMap.deserialize_model(api_response)
    chart = SymbolMap(**init_data)

    assert chart.basemap == "europe-nuts3-2021"
    assert chart.show_shape == "arrow"
    assert chart.max_size == 35
    assert chart.opacity == 1
    assert chart.multiply is False
    assert chart.hide_region_borders is True

    assert chart.lat == "LAT"
    assert chart.lon == "LON"
    assert chart.area == "pct_change"
    assert chart.address == "geo"
