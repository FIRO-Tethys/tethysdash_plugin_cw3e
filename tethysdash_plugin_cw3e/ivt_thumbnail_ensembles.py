from intake.source import base


class IVTThumbnailEnsembles(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "cw3e_ivt_thumbnail_ensembles"
    visualization_tags = [
        "cw3e",
        "ar",
        "ivt",
        "gefs",
        "ecmwf",
        "thumbnails",
    ]
    visualization_description = "Collection of thumbnails depicting IVT exceeding thresholds for each ensemble. More information can be found at https://cw3e.ucsd.edu/iwv-and-ivt-forecasts/"
    visualization_args = {
        "model": ["GEFS", "ECMWF EPS"],
        "forecast_hour": list(range(0, 366, 6)),
        "domain": [
            "Northeast Pacific",
            "U.S. West Coast",
            "Interior West",
            "North America",
        ],
    }
    visualization_group = "CW3E"
    visualization_label = "IVT Thumbnail Ensembles"
    visualization_type = "image"

    def __init__(self, model, forecast_hour, domain, metadata=None):
        # store important kwargs
        if model == "GEFS":
            self.model_location = "gefs/IVT_maps/GEFS"
        elif model == "ECMWF EPS":
            self.model_location = "ECMWF/IVT_Ensemble_Maps/ECMWF"

        self.forecast_hour = forecast_hour

        if domain == "Northeast Pacific":
            self.domain = "NEPac"
        elif domain == "U.S. West Coast":
            self.domain = "USWC"
        elif domain == "Interior West":
            self.domain = "IntWest"
        elif domain == "North America":
            self.domain = "NAmerica"
        super().__init__(metadata=metadata)

    def read(self):
        return f"https://cw3e.ucsd.edu/images/{self.model_location}_IVTThumbs_{self.domain}-F{self.forecast_hour}.png"
