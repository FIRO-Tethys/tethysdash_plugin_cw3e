from tethysapp.tethysdash.plugin_helpers import LayerConfigurationBuilder, TethysDashPlugin


class NOAACPC_30_DayPrecipOutlookLayer(TethysDashPlugin):
    name = "noaa_cpc_30_day_precip_outlook_layer"
    args = {}
    group = "NOAA"
    label = "CPC 30 Day Precipitation Outlook"
    type = "map_layer"
    tags = ["noaa", "map", "map_layer", "precipitation"]
    description = "The CPC Monthly Precipitation Outlook Web Service consist of NWS' Climate Prediction Center's Forecasted Precipitation Probabilities for US Weather Outlook polygon layer for One Calendar Month. More information can be found at https://mapservices.weather.noaa.gov/vector/rest/services/outlooks/cpc_mthly_precip_outlk/MapServer"
    attribution = "NOAA"

    def run(self):
        """
        Return map layer configuration
        """
        builder = LayerConfigurationBuilder(
            name="CPC 30 Day Precipitation Outlook",
            layer_source="ESRI Image and Map Service",
        )
        builder.set_source_properties(
            url="https://mapservices.weather.noaa.gov/vector/rest/services/outlooks/cpc_mthly_precip_outlk/MapServer",
        )
        builder.set_legend("default")

        return builder.build()
