from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin


class RadiometricWindProfilers(TethysDashPlugin):
    name = "cw3e_radiometric_wind_profilers"
    tags = [
        "cw3e",
        "radiometric",
        "wind",
        "profilers",
    ]
    description = "Plots show wind barbs depicting the horizontal wind speed and direction, colored based on wind speed (knots) at the selected location over the previous 48 hours (x-axis) from the surface up to 3 km above ground level (y-axis). The top panel shows a scatter plot of rain intensity (mm/h), the middle panel shows the radar reflectivity (dBZ), and the bottom panel shows the drop size distribution. More information can be found at https://cw3e.ucsd.edu/cw3e_observations_wind_profilers/"
    args = {"display_type": ["Plot", "Map"]}
    group = "CW3E"
    label = "Radiometric Wind Profilers"
    type = "image"
    attribution = "CW3E"

    def run(self):
        if self.display_type == "Map":
            return "https://cw3e.ucsd.edu/images/CW3E_Obs/maps/CW3E_Obs_WindProfiler_BFS.png"

        return (
            "https://cw3e.ucsd.edu/images/CW3E_Obs/BFS_Latest_Winds_interp_hourly.png"
        )
