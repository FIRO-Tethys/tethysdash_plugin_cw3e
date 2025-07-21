from intake.source import base


class RadiometricWindProfilersChart(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "dradiometric_wind_profilers_chart"
    visualization_tags = [
        "cw3e",
        "radiometric",
        "wind",
        "profilers",
    ]
    visualization_description = "Plots show wind barbs depicting the horizontal wind speed and direction, colored based on wind speed (knots) at the selected location over the previous 48 hours (x-axis) from the surface up to 3 km above ground level (y-axis). The top panel shows a scatter plot of rain intensity (mm/h), the middle panel shows the radar reflectivity (dBZ), and the bottom panel shows the drop size distribution. More information can be found at https://cw3e.ucsd.edu/cw3e_observations_wind_profilers/"
    visualization_args = {}
    visualization_group = "CW3E"
    visualization_label = "Radiometric Wind Profilers Plot"
    visualization_type = "image"

    def __init__(self, metadata=None):
        # store important kwargs
        super().__init__(metadata=metadata)

    def read(self):

        return (
            f"https://cw3e.ucsd.edu/images/CW3E_Obs/BFS_Latest_Winds_interp_hourly.png"
        )
