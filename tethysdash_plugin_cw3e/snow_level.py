from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin


class SnowLevel(TethysDashPlugin):
    name = "noaa_snow_level"
    tags = ["cw3e", "noaa", "snow", "level"]
    description = "Shows data from various snow level radars. Each plot shows color shading of vertical radial velocity or reflectivity and circles depicting the snow level indicated by a radar bright band when bright band precipitation is present. More information can be found at https://cw3e.ucsd.edu/real-time-observations/"
    args = {
        "location": [
            {"label": "Colfax", "value": "cff"},
            {"label": "Cazadero", "value": "czc"},
            {"label": "Downieville", "value": "dla"},
            {"label": "Granite Portal", "value": "gpo"},
            {"label": "Happy Camp", "value": "hcp"},
            {"label": "Headworks", "value": "hdw"},
            {"label": "Ingram", "value": "igm"},
            {"label": "Kernville", "value": "knv"},
            {"label": "Martis Creek", "value": "mak"},
            {"label": "Middletown", "value": "mdt"},
            {"label": "New Bullards Bar", "value": "nbb"},
            {"label": "New Exchequer Dam", "value": "ner"},
            {"label": "Oroville", "value": "ovl"},
            {"label": "Pine Flat Dam", "value": "pfd"},
            {"label": "Potter Valley Central", "value": "pvc"},
            {"label": "Saint Helena", "value": "sth"},
            {"label": "San Bernardino", "value": "sbo"},
            {"label": "San Luis Reservoir", "value": "slr"},
            {"label": "Santa Rosa", "value": "str"},
            {"label": "Shasta Dam", "value": "std"},
            {"label": "Seven Oaks Dam", "value": "sod"},
            {"label": "Twitchell Island", "value": "tci"},
        ],
        "display_type": [
            {"label": "Map", "value": "Map"},
            {
                "label": "Plot",
                "value": "Plot",
                "sub_args": {
                    "data_source": [
                        {"label": "Vertical Velocity", "value": "melt"},
                        {"label": "Reflectivity", "value": "snr"},
                    ],
                },
            },
        ],
    }
    group = "NOAA"
    label = "Snow Level Radars"
    type = "image"
    attribution = "NOAA"

    def __init__(self, location, display_type, metadata=None, **kwargs):
        # store important kwargs
        self.location = location
        self.display_type = display_type
        self.data_source = kwargs.get("display_type.data_source")
        super().__init__(metadata=metadata)

    def run(self):
        if self.display_type == "Map":
            return f"https://cw3e.ucsd.edu/images/aro/maps/slr_{self.location}.png"

        if self.location in ["dla", "gpo", "hdw", "igm", "mak", "nbb", "pvc", "sod"]:
            return f"https://cw3e.ucsd.edu/images/CW3E_Obs/{self.location.upper()}_MRR_48hr_latest.jpg"

        if self.data_source == "snr":
            return f"https://cw3e.ucsd.edu/images/aro/images/{self.location}_snr.gif"

        return f"https://cw3e.ucsd.edu/images/aro/images/{self.location}_melt.gif"
