from intake.source import base
from .constants import DISDROMETER_LOCATIONS


class DisdrometerChart(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "disdrometer_chart"
    visualization_tags = [
        "cw3e",
        "disdrometer",
        "rain",
        "precipitation",
    ]
    visualization_description = "Plots show data collected from a disdrometer deployed by CW3E. The top panel shows a scatter plot of rain intensity (mm/h), the middle panel shows the radar reflectivity (dBZ), and the bottom panel shows the drop size distribution. More information about Disrometer products can be found at https://cw3e.ucsd.edu/cw3e_observations_disdrometers/"
    visualization_args = {
        "location": DISDROMETER_LOCATIONS,
    }
    visualization_group = "CW3E"
    visualization_label = "Disdrometer Plot"
    visualization_type = "image"

    def __init__(self, location, metadata=None):
        # store important kwargs
        self.location = location
        super().__init__(metadata=metadata)

    def read(self):

        return f"https://cw3e.ucsd.edu/images/CW3E_Obs/{self.location}_Disdrometer_latest.jpg"
