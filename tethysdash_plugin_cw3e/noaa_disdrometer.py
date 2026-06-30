from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin


class NOAADisdrometer(TethysDashPlugin):
    name = "noaa_disdrometer"
    tags = [
        "cw3e",
        "noaa",
        "disdrometer",
        "rain",
        "precipitation",
    ]
    description = "Shows a comparison between S-band radar at multiple sites and the 0.5° elevation scan from the Sacramento, Ca WSR-88D scanning radar, as well as disdrometer and tipping bucket rain gauge data. More information can be found at https://cw3e.ucsd.edu/real-time-observations/"
    args = {
        "location": [
            {"label": "Bodega Bay, CA", "value": "bby"},
            {"label": "Cazadero, CA", "value": "czc"},
            {"label": "Los Gatos, CA", "value": "lgs"},
            {"label": "Middletown, CA", "value": "mdt"},
            {"label": "Santa Rosa, CA", "value": "str"},
            {"label": "Twitchell Island, CA", "value": "tci"},
        ],
        "display_type": ["Plot", "Map"],
    }
    group = "NOAA"
    label = "Disdrometer"
    type = "image"
    attribution = "NOAA"

    def run(self):
        if self.display_type == "Map":
            return f"https://cw3e.ucsd.edu/images/aro/maps/disd_{self.location}.png"

        return f"https://cw3e.ucsd.edu/images/aro/images/{self.location}_latest_PrecipAnalysis.gif"
