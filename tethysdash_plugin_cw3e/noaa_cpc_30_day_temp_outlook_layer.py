from intake.source import base
from tethysapp.tethysdash.plugin_helpers import LayerConfigurationBuilder


class NOAACPC_30_DayTempOutlookLayer(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "noaa_cpc_30_day_temp_outlook_layer"
    visualization_args = {}
    visualization_group = "NOAA"
    visualization_label = "CPC 30 Day Temperature Outlook"
    visualization_type = "map_layer"
    visualization_tags = ["noaa", "map", "map_layer", "temperature"]
    visualization_description = "Climate Predictive Center (CPC) Monthly Temperature Outlook Web Service consist of polygon layers of temperature forecast probabilities for the U.S. for the next calendar month. More information can be found at https://mapservices.weather.noaa.gov/vector/rest/services/outlooks/cpc_mthly_temp_outlk/MapServer"

    def __init__(self, metadata=None, **kwargs):
        super().__init__(metadata=metadata)

    def read(self):
        """
        Return map layer configuration
        """
        builder = LayerConfigurationBuilder(
            name="CPC 30 Day Temperature Outlook",
            layer_source="ESRI Image and Map Service",
        )
        builder.set_source_properties(
            url="https://mapservices.weather.noaa.gov/vector/rest/services/outlooks/cpc_mthly_temp_outlk/MapServer",
        )
        builder.set_legend("default")

        return builder.build()
