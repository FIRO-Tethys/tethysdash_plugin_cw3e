from intake.source import base


class IVTCrossSections(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "cw3e_ivt_cross_sections"
    visualization_tags = [
        "cw3e",
        "cross",
        "sections",
        "ivt",
    ]
    visualization_description = "Cross sections that illustrate the forecasted conditions along a longitudinal line from 25-65°N for the given forecast time from the GFS or ECMWF deterministic model.  More information can be found at https://cw3e.ucsd.edu/iwv-and-ivt-forecasts/"
    visualization_args = {
        "model": ["GFS", "ECMWF"],
        "longitude": [
            {"value": lon, "label": f"{lon} W"} for lon in range(105, 180, 5)
        ],
        "forecast_hour": [
            {"value": f"{hour:03}", "label": hour} for hour in range(0, 132, 12)
        ],
    }
    visualization_group = "CW3E"
    visualization_label = "IVT and Relative Humidity Plots"
    visualization_type = "image"

    def __init__(self, model, longitude, forecast_hour, metadata=None):
        # store important kwargs
        self.longitude = longitude
        self.model = model
        self.forecast_hour = forecast_hour

        super().__init__(metadata=metadata)

    def read(self):

        url_location = self.model
        if self.model == "GFS":
            url_location = "gfs"

        return f"https://cw3e.ucsd.edu/images/{url_location}/Cross_Sections/Cross_Section_latest_25-65N_{self.longitude}W_F{self.forecast_hour}.png"
