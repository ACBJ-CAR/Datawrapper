"""Integration tests for choropleth map serialization and deserialization."""

import json
from pathlib import Path

from datawrapper import ChoroplethMap


def load_sample_json(filename: str) -> dict:
    """Load a sample JSON file from tests/samples/choropleth_map/."""
    samples_dir = (
        Path(__file__).parent.parent
        / "samples"
        / "choropleth_map"
        / "tests"
        / "samples"
        / "choropleth_map"
    )
    with open(samples_dir / filename) as f:
        return json.load(f)


class TestChoroplethMapMigrationSample:
    """Tests migration sample coverage for choropleth-only features."""

    def test_deserialize_migratation_json_supports_legends_patterns_colorscale(self):
        """Ensure migration sample fields are parsed into the model init data."""
        sample_json = load_sample_json("migratation.json")
        chart_metadata = sample_json["chart"]["crdt"]["data"]

        init_data = ChoroplethMap.deserialize_model(chart_metadata)

        assert init_data["keys_column"] == "msa_code"
        assert init_data["values_column"] == "agi_net"
        assert init_data["pattern_column"] == "is_market"

        assert init_data["legends"]["color"]["title"] == "Net AGI"
        assert init_data["patterns"]["enabled"] is True
        assert init_data["patterns"]["map"]["True"]["label"] == "Memphis metro"
        assert init_data["colorscale"]["mode"] == "discrete"
        assert init_data["colorscale"]["stops"] == "custom"

    def test_round_trip_preserves_migration_fields(self):
        """Ensure deserialize -> serialize keeps legends, patterns, and colorscale unchanged."""
        sample_json = load_sample_json("migratation.json")
        chart_metadata = sample_json["chart"]["crdt"]["data"]
        sample_axes = chart_metadata["metadata"]["axes"]
        sample_visualize = chart_metadata["metadata"]["visualize"]

        chart = ChoroplethMap(**ChoroplethMap.deserialize_model(chart_metadata))
        serialized = chart.serialize_model()

        axes = serialized["metadata"]["axes"]
        visualize = serialized["metadata"]["visualize"]

        assert axes["pattern"] == sample_axes["pattern"]
        assert visualize["legends"] == sample_visualize["legends"]
        assert visualize["patterns"] == sample_visualize["patterns"]
        assert visualize["colorscale"] == sample_visualize["colorscale"]

    def test_explicit_colorscale_is_not_overwritten(self):
        """Ensure user-provided colorscale takes precedence over generated values."""
        explicit_colorscale = {
            "mode": "discrete",
            "stops": "custom",
            "interpolation": "equidistant",
            "colors": [
                {"color": "#111111", "position": 0},
                {"color": "#999999", "position": 1},
            ],
        }

        chart = ChoroplethMap(
            title="Test",
            keys_column="region",
            values_column="value",
            color_from="#000000",
            color_to="#ffffff",
            color_mode="buckets",
            colorscale=explicit_colorscale,
        )

        serialized = chart.serialize_model()
        assert serialized["metadata"]["visualize"]["colorscale"] == explicit_colorscale
