from intake.source import base
from tethysapp.tethysdash.plugin_helpers import LayerConfigurationBuilder


class SnowLevelRadarLayer(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "cw3e_snow_level_radar_layer"
    visualization_args = {}
    visualization_group = "CW3E"
    visualization_label = "Snow Level Radar Layer"
    visualization_type = "map_layer"
    visualization_tags = ["cw3e", "map", "map_layer", "snow", "level", "radar"]
    visualization_description = "A collection of points used for Snow Level Radar. More information can be found at https://cw3e.ucsd.edu/DSMaps/DS_freezing.html"

    def __init__(self, metadata=None, **kwargs):
        super().__init__(metadata=metadata)

    def read(self):
        """
        Return map layer configuration
        """
        builder = LayerConfigurationBuilder(
            name="Snow Level Radars", layer_source="GeoJSON"
        )
        builder.set_geojson("/static/tethysdash/data/plugins/radar_points.geojson")
        builder.set_style("/static/tethysdash/data/plugins/radar_points_styles.json")
        builder.add_attribute_variable(
            "reflectivity_url", "reflectivity_url", "Snow Level Radars"
        )
        builder.add_attribute_variable("melt_url", "melt_url", "Snow Level Radars")

        return builder.build()
