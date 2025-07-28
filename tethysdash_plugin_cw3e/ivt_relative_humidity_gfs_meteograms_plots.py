from intake.source import base


class IVTAndRelativeHumidityPlots(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "cw3e_ivt_and_relative_humidity_plots"
    visualization_tags = [
        "cw3e",
        "ar",
        "relative",
        "humidity",
        "ivt",
    ]
    visualization_description = "Meteograms that illustrate the forecasted conditions over a given locations for the 3 or 7-day forecast period from the GFS. The top panel includes water vapor flux (kg m-2s-1) or relative humidity (%) shaded with the 0°C isotherm contour and wind barbs(m/s), gray shading indicates location elevation. The middle plot illustrates the 3-hour precipitation represented by the bars, total 72-hour precipitation, height of the 0oC isotherm, and location elevation. When the freezing level is below the location elevation, line and bars are blue representing the likelihood of snow and when the freezing level is above the location elevation line and bars are green representing the likelihood of rain. The bottom plot illustrates the IWV and IVT, as well as the presence of AR conditions shaded in gray. More information can be found at https://cw3e.ucsd.edu/iwv-and-ivt-forecasts/"
    visualization_args = {
        "latitude": [{"value": lat, "label": f"{lat} N"} for lat in range(26, 51)],
        "longitude": [{"value": lon, "label": f"{lon} W"} for lon in range(111, 128)],
        "visualization": [
            "Map",
            {
                "value": "Plot",
                "label": "Plot",
                "sub_args": {
                    "model": ["GFS", "ECMWF"],
                    "plot_type": [
                        {"value": "3DayWVFlux", "label": "3-day WV Flux"},
                        {"value": "3DayRH", "label": "3-day Relative Humidity"},
                        {"value": "7DayWVFlux", "label": "7-day WV Flux"},
                        {"value": "7DayRH", "label": "7-day Relative Humidity"},
                    ],
                },
            },
        ],
    }
    visualization_group = "CW3E"
    visualization_label = "IVT and Relative Humidity Plots"
    visualization_type = "image"

    def __init__(self, latitude, longitude, visualization, metadata=None, **kwargs):
        # store important kwargs
        self.latitude = latitude
        self.longitude = longitude
        self.visualization = visualization
        self.model = kwargs.get("visualization.model")
        self.plot_type = kwargs.get("visualization.plot_type")

        if int(longitude) < 0:
            self.longitude = int(longitude) * -1
        super().__init__(metadata=metadata)

    def read(self):

        url_location = self.model
        if self.model == "GFS":
            url_location = "gfs"

        if self.visualization == "Map":
            return f"https://cw3e.ucsd.edu/images/gfs/Meteograms/maps/Meteo_maps{self.latitude}_{self.longitude}.png"

        return f"https://cw3e.ucsd.edu/images/{url_location}/Meteograms/{self.model}_{self.plot_type}_{self.latitude}N_{self.longitude}W.png"
