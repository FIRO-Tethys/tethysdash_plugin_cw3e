from tethysapp.tethysdash.plugin_helpers import LayerConfigurationBuilder, TethysDashPlugin


class IVTAndRelativeHumidityPoints(TethysDashPlugin):
    name = "cw3e_ivt_and_relative_humidity_points"
    args = {}
    group = "CW3E"
    label = "IVT and Relative Humidity Points"
    type = "map_layer"
    tags = [
        "cw3e",
        "map",
        "map_layer",
        "landfall",
        "ar",
        "ivt",
        "relative",
        "humidity",
    ]
    description = "A collection of points used for IVT and Relative Humidity plots. More information can be found at https://cw3e.ucsd.edu/iwv-and-ivt-forecasts/"
    attribution = "CW3E"

    def run(self):
        """
        Return map layer configuration
        """
        geojson_data = {
            "type": "FeatureCollection",
            "crs": {"properties": {"name": "EPSG:4326"}},
            "features": [],
        }

        for lat in range(26, 51):  # Latitude from 26 to 50 inclusive
            for lon in range(-127, -110):  # Longitude from -127 to -111 inclusive
                feature = {
                    "type": "Feature",
                    "properties": {"lat": str(lat), "lon": str(lon)},
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat],  # [longitude, latitude]
                    },
                }
                geojson_data["features"].append(feature)

        builder = LayerConfigurationBuilder(
            name="IVT Points",
            layer_source="GeoJSON",
        )
        builder.set_geojson(geojson_data)
        builder.add_attribute_variable("lat", "LAT", "IVT Points")
        builder.add_attribute_variable("lon", "LON", "IVT Points")
        builder.omit_popup_attribute("lat", "IVT Points")
        builder.omit_popup_attribute("lon", "IVT Points")

        return builder.build()
