from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin


class LandfallingARScaleFrequencyPlots(TethysDashPlugin):
    name = "cw3e_landfalling_ar_scale_frequency_plots"
    tags = [
        "cw3e",
        "ar",
        "landfall",
        "frequency",
        "probability",
        "coastal",
    ]
    description = "Frequency of AR events Plots. Includes Annual and Monthly frequencies as well as historical analysis. More information can be found at https://cw3e.ucsd.edu/Projects/ARCatalog/catalog.html"
    args = {
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
    group = "CW3E"
    label = "AR Landfall Frequencies"
    type = "image"
    attribution = "CW3E"

    def run(self):

        return f"https://cw3e.ucsd.edu/Projects/ARCatalog/images/{self.plot_type}-{self.latitude}.png"
