from intake.source import base
from .constants import MRR_LOCATIONS


class MicroRainRadarsChart(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "micro_rain_radars_chart"
    visualization_tags = [
        "cw3e",
        "micro",
        "rain",
        "precipitation",
        "radar",
    ]
    visualization_description = "Plots show data collected from the MRR station highlighted on the map. The top panel shows reflectivity shaded by color and the bottom panel shows vertical velocity. More information about MicroRain Radar products can be found at https://cw3e.ucsd.edu/cw3e_observations_disdrometers/"
    visualization_args = {
        "location": MRR_LOCATIONS,
    }
    visualization_group = "CW3E"
    visualization_label = "MicroRain Radar Plot"
    visualization_type = "image"

    def __init__(self, location, metadata=None):
        # store important kwargs
        self.location = location
        super().__init__(metadata=metadata)

    def read(self):

        return f"https://cw3e.ucsd.edu/images/CW3E_Obs/{self.location}_MRR_latest.jpg"
