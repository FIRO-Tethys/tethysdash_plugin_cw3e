from tethysapp.tethysdash.plugin_helpers import LayerConfigurationBuilder, TethysDashPlugin


class NOAACPC_30_DayTempOutlookLayer(TethysDashPlugin):
    name = "noaa_cpc_30_day_temp_outlook_layer"
    args = {}
    group = "NOAA"
    label = "CPC 30 Day Temperature Outlook"
    type = "map_layer"
    tags = ["noaa", "map", "map_layer", "temperature"]
    description = "Climate Predictive Center (CPC) Monthly Temperature Outlook Web Service consist of polygon layers of temperature forecast probabilities for the U.S. for the next calendar month. More information can be found at https://mapservices.weather.noaa.gov/vector/rest/services/outlooks/cpc_mthly_temp_outlk/MapServer"
    attribution = "NOAA"

    def run(self):
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
