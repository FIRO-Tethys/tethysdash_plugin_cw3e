from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin
from .constants import SurfaceMeterologyLocations


class SurfaceMeterology(TethysDashPlugin):
    name = "cw3e_surface_meterology"
    tags = [
        "cw3e",
        "temperature",
        "watershed",
        "temperature",
        "humidity",
        "sea level pressure",
        "solar radiation",
        "wind speed",
        "direction",
        "precipitation",
        "soil moisture",
        "soil temperature",
    ]
    description = "Surface meteorological and soil data observed at the specified location. Image includes charts for temperature and relative humidity, sea level pressure and solar radiation, wind speed and direction, hourly precipitation and accumulated precipitation, soil moisture at various depths, and soil temperature at the same depths as soil moisture. More information can be found at https://cw3e.ucsd.edu/cw3e_observations_surfacemet/"
    args = {
        "watershed_location": SurfaceMeterologyLocations,
    }
    group = "CW3E"
    label = "Surface Meteorology"
    type = "image"
    attribution = "CW3E"

    def run(self):

        return f"https://cw3e.ucsd.edu/images/CW3E_Obs/{self.watershed_location}_Latest_SurfaceMet.png"
