from intake.source import base
from tethysapp.tethysdash.exceptions import VisualizationError


class Temperature850hPA(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "cw3e_850_hpa_temperature"
    visualization_tags = [
        "cw3e",
        "gfs",
        "ecmwf",
        "temperature",
    ]
    visualization_description = "850-hPa temperature shaded in °C, heights contoured in geopotential meters and winds from the Global Forecast System (GFS). More information can be found at https://cw3e.ucsd.edu/850Temp_NEPac/"
    visualization_args = {
        "model": ["GFS", "ECMWF"],
        "forecast_hour": "text",
        "region": [
            {"value": "NPac", "label": "North Pacific"},
            {"value": "NEPac", "label": "Northeast Pacific"},
            {"value": "USWC", "label": "U.S. West Coast"},
            {"value": "NAmerica", "label": "North America"},
        ],
    }
    visualization_group = "CW3E"
    visualization_label = "850-hPa Temperature Model Analysis and Forecasts"
    visualization_type = "image"
    visualization_loading_icon = False

    def __init__(self, model, forecast_hour, region, metadata=None):
        # store important kwargs
        self.model = model
        self.forecast_hour = forecast_hour
        self.region = region
        super().__init__(metadata=metadata)

    def read(self):

        model_location = "gfs" if self.model == "GFS" else "ECMWF"

        return f"https://cw3e.ucsd.edu/images/{model_location}/850Temp/{self.model}_850Temp_{self.region}_latest_F{self.forecast_hour}.png"
