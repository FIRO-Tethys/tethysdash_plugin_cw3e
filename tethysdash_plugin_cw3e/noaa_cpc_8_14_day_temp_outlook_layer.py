from intake.source import base
from tethysapp.tethysdash.plugin_helpers import LayerConfigurationBuilder


class NOAACPC_8_14_DayTempOutlookLayer(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "noaa_cpc_8_14_day_temp_outlook_layer"
    visualization_args = {}
    visualization_group = "NOAA"
    visualization_label = "CPC 8-14 Day Temperature Outlook"
    visualization_type = "map_layer"
    visualization_tags = ["noaa", "map", "map_layer", "temperature"]
    visualization_description = "The CPC 8 to 14 Day Outlook Web Service consist of Forecasted US Weather Outlooks polygon layers of temperature for the U.S. for 8-14 days. More information can be found at https://mapservices.weather.noaa.gov/vector/rest/services/outlooks/cpc_8_14_day_outlk/MapServer"

    def __init__(self, metadata=None, **kwargs):
        super().__init__(metadata=metadata)

    def read(self):
        """
        Return map layer configuration
        """
        builder = LayerConfigurationBuilder(
            name="CPC 8-14 Day Temperature Outlook",
            layer_source="ESRI Image and Map Service",
        )
        builder.set_source_properties(
            url="https://mapservices.weather.noaa.gov/vector/rest/services/outlooks/cpc_8_14_day_outlk/MapServer",
            params={"LAYERS": "show:0"},
        )
        builder.set_legend("default")

        return builder.build()
