from intake.source import base


class NOAADisdrometer(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "noaa_disdrometer"
    visualization_tags = [
        "cw3e",
        "noaa",
        "disdrometer",
        "rain",
        "precipitation",
    ]
    visualization_description = "Shows a comparison between S-band radar at multiple sites and the 0.5° elevation scan from the Sacramento, Ca WSR-88D scanning radar, as well as disdrometer and tipping bucket rain gauge data. More information can be found at https://cw3e.ucsd.edu/real-time-observations/"
    visualization_args = {
        "location": [
            {"label": "Bodega Bay, CA", "value": "bby"},
            {"label": "Cazadero, CA", "value": "czc"},
            {"label": "Los Gatos, CA", "value": "lgs"},
            {"label": "Middletown, CA", "value": "mdt"},
            {"label": "Santa Rosa, CA", "value": "str"},
            {"label": "Twitchell Island, CA", "value": "tci"},
        ],
        "type": ["Plot", "Map"],
    }
    visualization_group = "NOAA"
    visualization_label = "Disdrometer"
    visualization_type = "image"

    def __init__(self, location, type, metadata=None):
        # store important kwargs
        self.location = location
        self.type = type
        super().__init__(metadata=metadata)

    def read(self):
        if self.type == "Map":
            return f"https://cw3e.ucsd.edu/images/aro/maps/disd_{self.location}.png"

        return f"https://cw3e.ucsd.edu/images/aro/images/{self.location}_latest_PrecipAnalysis.gif"
