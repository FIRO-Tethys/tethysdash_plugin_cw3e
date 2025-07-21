from intake.source import base
from .constants import DISDROMETER_LOCATIONS


class DisdrometerMap(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "disdrometer_map"
    visualization_tags = [
        "cw3e",
        "disdrometer",
        "rain",
        "precipitation",
    ]
    visualization_description = "Displays a png of a location map for the Disdrometer data. More information about Disdrometer products can be found at https://cw3e.ucsd.edu/cw3e_observations_disdrometers/"
    visualization_args = {
        "location": DISDROMETER_LOCATIONS,
    }
    visualization_group = "CW3E"
    visualization_label = "Disdrometer Map"
    visualization_type = "image"

    def __init__(self, location, metadata=None):
        # store important kwargs
        self.location = location
        super().__init__(metadata=metadata)

    def read(self):

        return f"https://cw3e.ucsd.edu/images/CW3E_Obs/maps/CW3E_Obs_DisdrometerMaps_{self.location}.png"
