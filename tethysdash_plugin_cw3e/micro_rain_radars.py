from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin
from .constants import MRR_LOCATIONS


class MicroRainRadars(TethysDashPlugin):
    name = "cw3e_micro_rain_radars"
    tags = [
        "cw3e",
        "micro",
        "rain",
        "precipitation",
        "radar",
    ]
    description = "Plots show data collected from the MRR station highlighted on the map. The top panel shows reflectivity shaded by color and the bottom panel shows vertical velocity. More information can be found at https://cw3e.ucsd.edu/cw3e_observations_mrrs/"
    args = {"location": MRR_LOCATIONS, "display_type": ["Plot", "Map"]}
    group = "CW3E"
    label = "MicroRain Radar"
    type = "image"
    attribution = "CW3E"

    def run(self):
        if self.display_type == "Map":
            return f"https://cw3e.ucsd.edu/images/CW3E_Obs/maps/CW3E_Obs_MRRMaps_{self.location}.png"

        return f"https://cw3e.ucsd.edu/images/CW3E_Obs/{self.location}_MRR_latest.jpg"
