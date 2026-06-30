from tethysapp.tethysdash.plugin_helpers import LayerConfigurationBuilder, TethysDashPlugin


class NOAACPCWeek1GFSAnomLayer(TethysDashPlugin):
    name = "noaa_cpc_week_1_gfs_precip_anom_layer"
    args = {}
    group = "NOAA"
    label = "CPC Week 1 GFS Precipitation Anomaly Analysis"
    type = "map_layer"
    tags = ["noaa", "map", "map_layer", "precipitation", "gfs"]
    description = "Climate Prediction Center’s Global Forecast System (GFS) Precipitation Anomaly Analysis Map Service’s consists of 7 day accumulated precipitation anomaly data from the Global Forecast System. More information can be found at https://mapservices.weather.noaa.gov/raster/rest/services/climate/cpc_gfs_precip_anom/MapServer"
    attribution = "NOAA"

    def run(self):
        """
        Return map layer configuration
        """
        builder = LayerConfigurationBuilder(
            name="CPC Week 1 GFS Precipitation Anomaly Analysis",
            layer_source="ESRI Image and Map Service",
        )
        builder.set_source_properties(
            url="https://mapservices.weather.noaa.gov/raster/rest/services/climate/cpc_gfs_precip_anom/MapServer",
            params={"LAYERS": "show:0"},
        )
        builder.set_legend("default")
        builder.set_opacity(0.5)

        return builder.build()
