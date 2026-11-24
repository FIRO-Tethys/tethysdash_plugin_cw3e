from tethysdash_plugin_cw3e.nws_radar_layer import NWSRadarLayer


def test_layer_points_at_the_nws_radar_map_service():
    config = NWSRadarLayer().run()

    assert config == {
        "configuration": {
            "type": "ImageLayer",
            "props": {
                "name": "NWS Radar Base Reflectivity",
                "source": {
                    "type": "ESRI Image and Map Service",
                    "props": {
                        "url": (
                            "https://mapservices.weather.noaa.gov/eventdriven/"
                            "rest/services/radar/radar_base_reflectivity/MapServer"
                        )
                    },
                },
                "opacity": 0.7,
            },
        },
    }
