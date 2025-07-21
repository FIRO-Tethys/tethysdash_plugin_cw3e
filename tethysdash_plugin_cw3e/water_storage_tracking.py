from intake.source import base


class WaterStorageTracking(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "water_storage_tracking"
    visualization_tags = ["cw3e", "storage", "reservoir"]
    visualization_description = "Shows the most recent summary of reservoir water storage and reservoir-plus-snowpack water storage  based on daily California Department of Water Resources’ reports of storage. More information can be found at https://cw3e.ucsd.edu/water_storage_tracking/"
    visualization_args = {
        "domain": [
            {"label": "Sierra", "value": "Sierra"},
            {"label": "North Sierra", "value": "NorthSierra"},
            {"label": "Central Sierra", "value": "CentralSierra"},
            {"label": "South Sierra", "value": "SouthSierra"},
            {"label": "Feather River", "value": "Feather"},
            {"label": "Lake Tahoe Basin", "value": "Tahoe"},
            {"label": "Upper Sacramento River", "value": "Shasta"},
            {"label": "Yuba River", "value": "Yuba"},
        ],
        "type": ["Plot", "Map"],
    }
    visualization_group = "CW3E"
    visualization_label = "Water Storage Tracking"
    visualization_type = "image"

    def __init__(self, domain, type, metadata=None):
        # store important kwargs
        self.type = type
        self.domain = domain
        super().__init__(metadata=metadata)

    def read(self):
        if self.type == "Map":
            if self.domain in ["Sierra", "CentralSierra"]:
                return f"https://cw3e.ucsd.edu/images/Reservoirs_Snow/{self.domain}_Reservoirs.png"

            if self.domain == "NorthSierra":
                return "https://cw3e.ucsd.edu/images/Reservoirs_Snow/NorthernCal_Reservoirs.png"

            if self.domain == "SouthSierra":
                return "https://cw3e.ucsd.edu/images/Reservoirs_Snow/SouthernSierra_Reservoirs.png"

            return f"https://cw3e.ucsd.edu/images/Reservoirs_Snow/{self.domain}_Reservoirs_Snotels.png"

        return f"https://cw3e.ucsd.edu/images/Reservoirs_Snow/{self.domain}_Reservoirs_Snow_Storage.png"
