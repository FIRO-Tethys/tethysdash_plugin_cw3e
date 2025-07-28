from intake.source import base
from .constants import AR_CATALOG_POINTS
from tethysapp.tethysdash.plugin_helpers import LayerConfigurationBuilder


class LandfallingARScaleFrequencyPoints(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "cw3e_landfalling_ar_scale_frequency_points"
    visualization_args = {}
    visualization_group = "CW3E"
    visualization_label = "Landfalling AR Scale Frequency Points"
    visualization_type = "map_layer"
    visualization_tags = ["cw3e", "map", "map_layer", "landfall", "ar"]
    visualization_description = "A collection of points used for AR Scale Frequency plots. More information can be found at https://cw3e.ucsd.edu/Projects/ARCatalog/catalog.html"

    def __init__(self, metadata=None, **kwargs):
        super().__init__(metadata=metadata)

    def read(self):
        """
        Return map layer configuration
        """
        builder = LayerConfigurationBuilder(
            name="Landfalling AR Points", layer_source="GeoJSON"
        )
        builder.set_geojson(AR_CATALOG_POINTS)
        builder.add_attribute_variable("lat", "LAT", "Landfalling AR Points")
        builder.omit_popup_attribute("lat", "Landfalling AR Points")

        return builder.build()
