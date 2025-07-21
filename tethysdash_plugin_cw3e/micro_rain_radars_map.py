from intake.source import base
from .constants import MRRS_LOCATIONS


class MicroRainRadarsMap(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "micro_rain_radars_map"
    visualization_tags = [
        "cw3e",
        "micro",
        "rain",
        "precipitation",
        "radar",
    ]
    visualization_description = "Displays a png of a location map for the MircoRain Radar. More information about MicroRain Radar products can be found at https://cw3e.ucsd.edu/cw3e_observations_mrrs/"
    visualization_args = {
        "location": MRRS_LOCATIONS,
    }
    visualization_group = "CW3E"
    visualization_label = "MicroRain Radar Map"
    visualization_type = "image"

    def __init__(self, location, metadata=None):
        # store important kwargs
        self.location = location
        super().__init__(metadata=metadata)

    def read(self):

        return f"https://cw3e.ucsd.edu//images/CW3E_Obs/maps/CW3E_Obs_MRRMaps_{self.location}.png"
