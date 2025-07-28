from intake.source import base


class LandfallingARScaleFrequencyPlots(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "cw3e_landfalling_ar_scale_frequency_plots"
    visualization_tags = [
        "cw3e",
        "ar",
        "landfall",
        "frequency",
        "probability",
        "coastal",
    ]
    visualization_description = "Frequency of AR events Plots. Includes Annual and Monthly frequencies as well as historical analysis. More information can be found at https://cw3e.ucsd.edu/Projects/ARCatalog/catalog.html"
    visualization_args = {
        "latitude": "text",
        "plot_type": [
            {"value": "annual/annualfreq", "label": "Annual AR Frequency"},
            {"value": "monthly/monthlyfreq", "label": "Monthly Average AR Frequency"},
            {
                "value": "radial/radial",
                "label": "Event Average IVT Magnitudes and Direction",
            },
            {
                "value": "radial/radialsummary",
                "label": "Event Frequency by IVT and AR Scale",
            },
        ],
    }
    visualization_group = "CW3E"
    visualization_label = "AR Landfall Frequencies"
    visualization_type = "image"

    def __init__(self, latitude, plot_type, metadata=None):
        # store important kwargs
        self.latitude = latitude
        self.plot_type = plot_type
        super().__init__(metadata=metadata)

    def read(self):

        return f"https://cw3e.ucsd.edu/Projects/ARCatalog/images/{self.plot_type}-{self.latitude}.png"
