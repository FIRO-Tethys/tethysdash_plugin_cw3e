from intake.source import base
import re


class IVTEnsembleProbability(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "cw3e_ivt_ensemble_probability"
    visualization_tags = [
        "cw3e",
        "ar",
        "ivt",
        "gefs",
        "ecmwf",
        "probability",
    ]
    visualization_description = "Probability of IVT exceeding thresholds based on the forecast members and ensemble mean IVT vectors. Right: ensemble member contours (thin lines) and ensemble mean (thick blue line). More information can be found at https://cw3e.ucsd.edu/iwv-and-ivt-forecasts/"
    visualization_args = {
        "model": ["GEFS", "ECMWF EPS"],
        "threshold": ["IVT >250 kg/m/s", "IVT >500 kg/m/s", "IVT >750 kg/m/s"],
        "forecast_hour": list(range(0, 246, 6)),
        "domain": [
            "Northeast Pacific",
            "U.S. West Coast",
            "Interior West",
            "North America",
        ],
        "plot_type": ["Probability", "Contours"],
    }
    visualization_group = "CW3E"
    visualization_label = "IVT Ensemble Probabilities"
    visualization_type = "image"

    def __init__(
        self, model, threshold, forecast_hour, domain, plot_type, metadata=None
    ):
        # store important kwargs
        if model == "GEFS":
            self.model_location = "gefs/IVT_maps/GEFS"
        elif model == "ECMWF EPS":
            self.model_location = "ECMWF/IVT_Ensemble_Maps/ECMWF"

        self.threshold = int(re.search(r"\d+", threshold).group())
        self.forecast_hour = forecast_hour

        if domain == "Northeast Pacific":
            self.domain = "NEPac"
        elif domain == "U.S. West Coast":
            self.domain = "USWC"
        elif domain == "Interior West":
            self.domain = "IntWest"
        elif domain == "North America":
            self.domain = "NAmerica"

        if plot_type == "Probability":
            self.plot_type = "Prob"
        elif plot_type == "Contours":
            self.plot_type = "Spag"
        super().__init__(metadata=metadata)

    def read(self):

        return f"https://cw3e.ucsd.edu/images/{self.model_location}_IVT{self.plot_type}_{self.threshold}_{self.domain}-F{self.forecast_hour}.png"
