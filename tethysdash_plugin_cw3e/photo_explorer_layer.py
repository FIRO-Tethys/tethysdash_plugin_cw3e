from intake.source import base
from tethysapp.tethysdash.plugin_helpers import LayerConfigurationBuilder


class USGSPhotoExplorerLayer(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "usgs_photo_explorer_layer"
    visualization_args = {}
    visualization_group = "USGS"
    visualization_label = "USGS Photo Explorer Layer"
    visualization_type = "map_layer"
    visualization_tags = ["usgs", "photo"]
    visualization_description = "A collection of points used for USGS Photo Explorer Sites. More information can be found at https://www.usgs.gov/apps/ecosheds/fpe/#/explorer"

    def __init__(self, metadata=None, **kwargs):
        super().__init__(metadata=metadata)

    def read(self):
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
