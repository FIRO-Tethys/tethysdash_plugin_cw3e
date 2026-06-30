from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin


class WaterStorageTracking(TethysDashPlugin):
    name = "cw3e_water_storage_tracking"
    tags = ["cw3e", "storage", "reservoir"]
    description = "Shows the most recent summary of reservoir water storage and reservoir-plus-snowpack water storage  based on daily California Department of Water Resources’ reports of storage. More information can be found at https://cw3e.ucsd.edu/water_storage_tracking/"
    args = {
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
        "display_type": ["Plot", "Map"],
    }
    group = "CW3E"
    label = "Water Storage Tracking"
    type = "image"
    attribution = "CW3E"

    def run(self):
        if self.display_type == "Map":
            if self.domain in ["Sierra", "CentralSierra"]:
                return f"https://cw3e.ucsd.edu/images/Reservoirs_Snow/{self.domain}_Reservoirs.png"

            if self.domain == "NorthSierra":
                return "https://cw3e.ucsd.edu/images/Reservoirs_Snow/NorthernCal_Reservoirs.png"

            if self.domain == "SouthSierra":
                return "https://cw3e.ucsd.edu/images/Reservoirs_Snow/SouthernSierra_Reservoirs.png"

            return f"https://cw3e.ucsd.edu/images/Reservoirs_Snow/{self.domain}_Reservoirs_Snotels.png"

        return f"https://cw3e.ucsd.edu/images/Reservoirs_Snow/{self.domain}_Reservoirs_Snow_Storage.png"
