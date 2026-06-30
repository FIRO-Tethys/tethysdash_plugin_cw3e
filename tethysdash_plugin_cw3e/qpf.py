from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin
from .constants import CW3EHUC8s, QPF_visualizations


class QPF(TethysDashPlugin):
    name = "cw3e_qpf"
    tags = ["cw3e", "qpf", "precipitation", "huc8"]
    description = "Depicts the mean areal precipiation (MAP) at different lead times from several numerical weather prediction models and NOAA/NWS forecasts. More information can be found at https://cw3e.ucsd.edu/Projects/QPF/QPF-HUC8.html"
    args = {
        "HUC8": CW3EHUC8s,
        "QPF_visualization": QPF_visualizations,
    }
    group = "CW3E"
    label = "10-day Model Precipitation Forecasts"
    type = "image"
    attribution = "CW3E"

    def run(self):
        """Return a version of the xarray with all the data in memory"""

        QPF_base_url = "https://cw3e.ucsd.edu/Projects/QPF/images/HUC8/"

        plot_type = {
            "10-Day Mean QPF Table": "table_",
            "10-Day Accumulated Ensemble QPF": "combo_",
            "10-Day 6-Hour Ensemble QPF": "grid_",
        }

        return QPF_base_url + plot_type[self.QPF_visualization] + self.HUC8 + ".png"
