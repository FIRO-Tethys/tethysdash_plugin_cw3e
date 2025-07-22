from intake.source import base
from .constants import MRR_LOCATIONS


class MicroRainRadars(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "cw3e_micro_rain_radars"
    visualization_tags = [
        "cw3e",
        "micro",
        "rain",
        "precipitation",
        "radar",
    ]
    visualization_description = "Plots show data collected from the MRR station highlighted on the map. The top panel shows reflectivity shaded by color and the bottom panel shows vertical velocity. More information can be found at https://cw3e.ucsd.edu/cw3e_observations_mrrs/"
    visualization_args = {"location": MRR_LOCATIONS, "type": ["Plot", "Map"]}
    visualization_group = "CW3E"
    visualization_label = "MicroRain Radar"
    visualization_type = "image"

    def __init__(self, location, type, metadata=None):
        # store important kwargs
        self.location = location
        self.type = type
        super().__init__(metadata=metadata)

    def read(self):
        if self.type == "Map":
            return f"https://cw3e.ucsd.edu/images/CW3E_Obs/maps/CW3E_Obs_MRRMaps_{self.location}.png"

        return f"https://cw3e.ucsd.edu/images/CW3E_Obs/{self.location}_MRR_latest.jpg"
