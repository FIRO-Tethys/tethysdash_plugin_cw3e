from intake.source import base


class RadiometricWindProfilersMap(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "radiometric_wind_profilers_map"
    visualization_tags = [
        "cw3e",
        "radiometric",
        "wind",
        "profilers",
    ]
    visualization_description = "Displays a png of a location map for the Radiometric Wind Profilers data. More information about Disrometer products can be found at https://cw3e.ucsd.edu/cw3e_observations_wind_profilers/"
    visualization_args = {}
    visualization_group = "CW3E"
    visualization_label = "Radiometric Wind Profilers Map"
    visualization_type = "image"

    def __init__(self, metadata=None):
        # store important kwargs
        super().__init__(metadata=metadata)

    def read(self):

        return (
            "https://cw3e.ucsd.edu/images/CW3E_Obs/maps/CW3E_Obs_WindProfiler_BFS.png"
        )
