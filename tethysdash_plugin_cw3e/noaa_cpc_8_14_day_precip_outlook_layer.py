from tethysapp.tethysdash.plugin_helpers import LayerConfigurationBuilder, TethysDashPlugin


class NOAACPC_8_14_DayPrecipOutlookLayer(TethysDashPlugin):
    name = "noaa_cpc_8_14_day_precip_outlook_layer"
    args = {}
    group = "NOAA"
    label = "CPC 8-14 Day Precipitation Outlook"
    type = "map_layer"
    tags = ["noaa", "map", "map_layer", "precipitation"]
    description = "The CPC 8 to 14 Day Outlook Web Service consist of Forecasted US Weather Outlooks polygon layers of precipitation for the U.S. for 8-14 days. More information can be found at https://mapservices.weather.noaa.gov/vector/rest/services/outlooks/cpc_8_14_day_outlk/MapServer"

    def run(self):
        """
        Return map layer configuration
        """
        builder = LayerConfigurationBuilder(
            name="CPC 8-14 Day Precipitation Outlook",
            layer_source="ESRI Image and Map Service",
        )
        builder.set_source_properties(
            url="https://mapservices.weather.noaa.gov/vector/rest/services/outlooks/cpc_8_14_day_outlk/MapServer",
            params={"LAYERS": "show:1"},
        )
        builder.set_legend("default")

        return builder.build()
