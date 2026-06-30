from tethysapp.tethysdash.plugin_helpers import LayerConfigurationBuilder, TethysDashPlugin


class USGSPhotoExplorerLayer(TethysDashPlugin):
    name = "usgs_photo_explorer_layer"
    args = {}
    group = "USGS"
    label = "USGS Photo Explorer Layer"
    type = "map_layer"
    tags = ["usgs", "photo"]
    description = "A collection of points used for USGS Photo Explorer Sites. More information can be found at https://www.usgs.gov/apps/ecosheds/fpe/#/explorer"

    def run(self):
        """
        Return map layer configuration
        """
        builder = LayerConfigurationBuilder(
            name="USGS Photo Explorer", layer_source="GeoJSON"
        )
        builder.set_geojson(
            "/static/tethysdash/data/plugins/photo_explorer_stations.geojson"
        )
        builder.add_attribute_variable("user_id", "user_id", "USGS Photo Explorer")
        builder.add_attribute_variable("id", "station_id", "USGS Photo Explorer")

        return builder.build()
