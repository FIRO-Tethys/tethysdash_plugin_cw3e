from intake.source import base


class SnowLevel(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "noaa_snow_level"
    visualization_tags = ["cw3e", "noaa", "snow", "level"]
    visualization_description = "Shows data from various snow level radars. Each plot shows color shading of vertical radial velocity or reflectivity and circles depicting the snow level indicated by a radar bright band when bright band precipitation is present. More information can be found at https://cw3e.ucsd.edu/real-time-observations/"
    visualization_args = {
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
        "type": [
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
    visualization_group = "NOAA"
    visualization_label = "Snow Level Radars"
    visualization_type = "image"

    def __init__(self, location, type, metadata=None, **kwargs):
        # store important kwargs
        self.location = location
        self.type = type
        self.data_source = kwargs.get("type.data_source")
        super().__init__(metadata=metadata)

    def read(self):
        if self.type == "Map":
            return f"https://cw3e.ucsd.edu/images/aro/maps/slr_{self.location}.png"

        if self.location in ["dla", "gpo", "hdw", "igm", "mak", "nbb", "pvc", "sod"]:
            return f"https://cw3e.ucsd.edu/images/CW3E_Obs/{self.location.upper()}_MRR_48hr_latest.jpg"

        if self.data_source == "snr":
            return f"https://cw3e.ucsd.edu/images/aro/images/{self.location}_snr.gif"

        return f"https://cw3e.ucsd.edu/images/aro/images/{self.location}_melt.gif"
