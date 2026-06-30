from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin
from .constants import DISDROMETER_LOCATIONS


class Disdrometer(TethysDashPlugin):
    name = "cw3e_disdrometer"
    tags = [
        "cw3e",
        "disdrometer",
        "rain",
        "precipitation",
    ]
    description = "Plots show data collected from a disdrometer deployed by CW3E. The top panel shows a scatter plot of rain intensity (mm/h), the middle panel shows the radar reflectivity (dBZ), and the bottom panel shows the drop size distribution. More information about Disrometer products can be found at https://cw3e.ucsd.edu/cw3e_observations_disdrometers/"
    args = {"location": DISDROMETER_LOCATIONS, "display_type": ["Plot", "Map"]}
    group = "CW3E"
    label = "Disdrometer"
    type = "image"
    attribution = "CW3E"

    def run(self):
        if self.display_type == "Map":
            return f"https://cw3e.ucsd.edu/images/CW3E_Obs/maps/CW3E_Obs_DisdrometerMaps_{self.location}.png"

        return f"https://cw3e.ucsd.edu/images/CW3E_Obs/{self.location}_Disdrometer_latest.jpg"
