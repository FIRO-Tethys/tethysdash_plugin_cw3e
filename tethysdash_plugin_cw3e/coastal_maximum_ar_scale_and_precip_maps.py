from intake.source import base


class CoastalMaximumARScaleAndPrecipMaps(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "cw3e_coastal_maximum_ar_scale_and_precip_maps"
    visualization_tags = [
        "cw3e",
        "ar",
        "landfall",
        "frequency",
        "probability",
        "coastal",
        "precipitation",
    ]
    visualization_description = "Represent the AR scale observed and forecast at each grid point. GEFS plots update about every six hours and ECMWF plots update about every 12 hours.. More information can be found at https://cw3e.ucsd.edu/arscale/"
    visualization_args = {
        "plot_type": ["Observed", "Control Forecast", "Ensemble Mean"],
        "show_precipitation": "checkbox",
        "model": ["European Model (ECMWF)", "U.S. National Model (GEFS)"],
        "location": ["Coastal", "Foothills", "Inland", "Interior West"],
    }
    visualization_group = "CW3E"
    visualization_label = "Coastal Maximum AR Scale and Precipitation Maps"
    visualization_type = "image"

    def __init__(self, plot_type, show_precipitation, model, location, metadata=None):
        # store important kwargs
        self.plot_type = plot_type
        self.show_precipitation = show_precipitation
        self.model = model
        self.location = location
        super().__init__(metadata=metadata)

    def read(self):

        precip_suffix = ""
        if not self.show_precipitation:
            precip_suffix = "_NoQPF"
            if self.plot_type == "Observed":
                precip_suffix = "_NoQPE"

        if self.model == "U.S. National Model (GEFS)":
            model_url = "gefs"
        elif self.model == "European Model (ECMWF)":
            model_url = "ECMWF"

        if self.location == "Coastal":
            location = "coast"
        elif self.location == "Foothills":
            location = "foothills"
        elif self.location == "Inland":
            location = "inland"
        elif self.location == "Interior West":
            location = "intwest"

        if self.plot_type == "Observed":
            plot_type = "Analysis"
        elif self.plot_type == "Control Forecast":
            plot_type = "Forecast_Control"
        elif self.plot_type == "Ensemble Mean":
            plot_type = "Forecast_Mean"

        return f"https://cw3e.ucsd.edu/images/{model_url}/ARScale/{location}/{model_url.upper()}_ARScaleMap_{plot_type}_{location}{precip_suffix}.png"
