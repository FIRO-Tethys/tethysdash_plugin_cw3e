from tethysapp.tethysdash.plugin_helpers import (
    LayerConfigurationBuilder,
    TethysDashPlugin,
)

RADAR_URL = (
    "https://mapservices.weather.noaa.gov/eventdriven/rest/services/radar/"
    "radar_base_reflectivity/MapServer"
)


class NWSRadarLayer(TethysDashPlugin):
    name = "nws_radar_base_reflectivity_layer"
    args = {}
    group = "NOAA"
    label = "NWS Radar Base Reflectivity"
    type = "map_layer"
    tags = ["noaa", "nws", "map", "map_layer", "radar", "precipitation"]
    description = (
        "Latest NWS weather radar base reflectivity, a 1 km mosaic of the "
        "WSR-88D radars from the Multi-Radar Multi-Sensor (MRMS) system, "
        "updated every 5 minutes. More information can be found at "
        f"{RADAR_URL}"
    )
    attribution = "NOAA"

    def run(self):
        """
        Return map layer configuration
        """
        builder = LayerConfigurationBuilder(
            name="NWS Radar Base Reflectivity",
            layer_source="ESRI Image and Map Service",
        )
        builder.set_source_properties(url=RADAR_URL)
        # No legend: the service's own lists its RGB bands and its hidden
        # boundary and footprint layers, and NWS publishes no dBZ scale for
        # its colors.
        builder.set_opacity(0.7)

        return builder.build()
