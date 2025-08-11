from intake.source import base
from tethysapp.tethysdash.exceptions import VisualizationError


class IVTAndIWVAnalysesAndForecasts(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "cw3e_ivt_and_iwv_analyses_and_forecasts"
    visualization_tags = [
        "cw3e",
        "ar",
        "ivt",
        "gfs",
        "ecmwf",
        "iwv",
    ]
    visualization_description = "Vertically Integrated Water Vapor Transport (IVT) with magnitude shaded in units of kg m-1 s-1, direction indicated by vectors and mean sea level pressure contoured in hPa. Integrated water vapor (IWV) with magnitude shaded in units of mm, 850-hPa wind vectors, and mean sea level pressure contoured in hPa. More information can be found at https://cw3e.ucsd.edu/ivt_iwv_npacific/"
    visualization_args = {
        "model": ["GFS", "ECMWF", "ECMWF-GFS"],
        "product": [{"value": "ivt", "label": "IVT"}, {"value": "iwv", "label": "IWV"}],
        "forecast_hour": "text",
        "region": [
            {"value": "NPac", "label": "North Pacific"},
            {"value": "NEPac", "label": "Northeast Pacific"},
            {"value": "USWC", "label": "U.S. West Coast"},
            {"value": "IntWest", "label": "Interior West"},
            {"value": "NAmerica", "label": "North America"},
            {"value": "NAtlantic", "label": "North Atlantic"},
        ],
    }
    visualization_group = "CW3E"
    visualization_label = "IVT and IWV Analyses and Forecasts"
    visualization_type = "image"
    visualization_loading_icon = False

    def __init__(self, model, product, forecast_hour, region, metadata=None):
        # store important kwargs
        self.model = model
        self.product = product
        self.forecast_hour = forecast_hour
        self.region = region
        super().__init__(metadata=metadata)

    def read(self):
        if self.model != "GFS" and self.region == "NAtlantic":
            raise VisualizationError(
                "ECMWF model is not available for the North Atlantic region."
            )
            
        if self.model == "ECMWF-GFS" and self.region == "NAmerica":
            raise VisualizationError(
                "ECMWF-GFS model is not available for the North America region."
            )

        model_location = "gfs" if self.model == "GFS" else "ECMWF"

        return f"https://cw3e.ucsd.edu/images/{model_location}/{self.product}/{self.model}_{self.product.upper() if self.model == "ECMWF-GFS" else self.product}_{self.region}_latest_F{self.forecast_hour}.png"
