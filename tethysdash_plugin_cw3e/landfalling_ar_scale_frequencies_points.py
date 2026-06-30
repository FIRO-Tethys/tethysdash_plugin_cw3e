from .constants import AR_CATALOG_POINTS
from tethysapp.tethysdash.plugin_helpers import LayerConfigurationBuilder, TethysDashPlugin


class LandfallingARScaleFrequencyPoints(TethysDashPlugin):
    name = "cw3e_landfalling_ar_scale_frequency_points"
    args = {}
    group = "CW3E"
    label = "Landfalling AR Scale Frequency Points"
    type = "map_layer"
    tags = ["cw3e", "map", "map_layer", "landfall", "ar"]
    description = "A collection of points used for AR Scale Frequency plots. More information can be found at https://cw3e.ucsd.edu/Projects/ARCatalog/catalog.html"
    attribution = "CW3E"

    def run(self):
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
