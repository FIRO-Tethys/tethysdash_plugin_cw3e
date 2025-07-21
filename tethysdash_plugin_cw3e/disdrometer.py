from intake.source import base
from .constants import DISDROMETER_LOCATIONS


class Disdrometer(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "disdrometer"
    visualization_tags = [
        "cw3e",
        "disdrometer",
        "rain",
        "precipitation",
    ]
    visualization_description = "Plots show data collected from a disdrometer deployed by CW3E. The top panel shows a scatter plot of rain intensity (mm/h), the middle panel shows the radar reflectivity (dBZ), and the bottom panel shows the drop size distribution. More information about Disrometer products can be found at https://cw3e.ucsd.edu/cw3e_observations_disdrometers/"
    visualization_args = {"location": DISDROMETER_LOCATIONS, "type": ["Plot", "Map"]}
    visualization_group = "CW3E"
    visualization_label = "Disdrometer"
    visualization_type = "image"

    def __init__(self, location, type, metadata=None):
        # store important kwargs
        self.location = location
        self.type = type
        super().__init__(metadata=metadata)

    def read(self):
        if self.type == "Map":
            return f"https://cw3e.ucsd.edu/images/CW3E_Obs/maps/CW3E_Obs_DisdrometerMaps_{self.location}.png"

        return f"https://cw3e.ucsd.edu/images/CW3E_Obs/{self.location}_Disdrometer_latest.jpg"
