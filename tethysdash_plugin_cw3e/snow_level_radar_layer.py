from tethysapp.tethysdash.plugin_helpers import LayerConfigurationBuilder, TethysDashPlugin


class SnowLevelRadarLayer(TethysDashPlugin):
    name = "cw3e_snow_level_radar_layer"
    args = {}
    group = "CW3E"
    label = "Snow Level Radar Layer"
    type = "map_layer"
    tags = ["cw3e", "map", "map_layer", "snow", "level", "radar"]
    description = "A collection of points used for Snow Level Radar. More information can be found at https://cw3e.ucsd.edu/DSMaps/DS_freezing.html"
    attribution = "CW3E"

    def run(self):
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
