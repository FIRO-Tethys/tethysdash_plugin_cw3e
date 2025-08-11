from intake.source import base
from tethysapp.tethysdash.exceptions import VisualizationError


class Vorticity500hPA(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "cw3e_500_hpa_vorticity"
    visualization_tags = [
        "cw3e",
        "gfs",
        "ecmwf",
        "vorticity",
    ]
    visualization_description = "500-hPa absolute vorticty shaded in x10-5 s-1, heights contoured in geopotential meters and winds from the Global Forecast System (GFS) and the European Centre for Medium-Range Weather Forecasts (ECMWF). More information can be found at https://cw3e.ucsd.edu/500Vort_NPac/"
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
    visualization_label = "500-hPa Absolute Vorticity Model Analysis and Forecasts"
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

        return f"https://cw3e.ucsd.edu/images/{model_location}/500Vort/{self.model}_500Vort_{self.region}_latest_F{self.forecast_hour}.png"
