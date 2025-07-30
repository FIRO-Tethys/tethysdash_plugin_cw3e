from intake.source import base
from tethysapp.tethysdash.plugin_helpers import LayerConfigurationBuilder


class NOAACPCWeek2GFSAnomLayer(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "noaa_cpc_week_2_gfs_precip_anom_layer"
    visualization_args = {}
    visualization_group = "NOAA"
    visualization_label = "CPC Week 2 GFS Precipitation Anomaly Analysis"
    visualization_type = "map_layer"
    visualization_tags = ["noaa", "map", "map_layer", "precipitation", "gfs"]
    visualization_description = "Climate Prediction Center’s Global Forecast System (GFS) Precipitation Anomaly Analysis Map Service’s consists of 7 day accumulated precipitation anomaly data from the Global Forecast System. More information can be found at https://mapservices.weather.noaa.gov/raster/rest/services/climate/cpc_gfs_precip_anom/MapServer"

    def __init__(self, metadata=None, **kwargs):
        super().__init__(metadata=metadata)

    def read(self):
        """
        Return map layer configuration
        """
        builder = LayerConfigurationBuilder(
            name="CPC Week 2 GFS Precipitation Anomaly Analysis",
            layer_source="ESRI Image and Map Service",
        )
        builder.set_source_properties(
            url="https://mapservices.weather.noaa.gov/raster/rest/services/climate/cpc_gfs_precip_anom/MapServer",
            params={"LAYERS": "show:1"},
        )
        builder.set_legend("default")
        builder.set_opacity(0.5)

        return builder.build()
