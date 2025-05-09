from intake.source import base
from .constants import SurfaceMeterologyLocations


class SurfaceMeterology(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "cw3e_surface_meterology"
    visualization_tags = [
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
    visualization_description = "Surface meteorological and soil data observed at the specified location. Image includes charts for temperature and relative humidity, sea level pressure and solar radiation, wind speed and direction, hourly precipitation and accumulated precipitation, soil moisture at various depths, and soil temperature at the same depths as soil moisture. More information can be found at https://cw3e.ucsd.edu/cw3e_observations_surfacemet/"
    visualization_args = {
        "watershed_location": SurfaceMeterologyLocations,
    }
    visualization_group = "CW3E"
    visualization_label = "Surface Meteorology"
    visualization_type = "image"

    def __init__(self, watershed_location, metadata=None):
        # store important kwargs
        self.watershed_location = watershed_location
        super(SurfaceMeterology, self).__init__(metadata=metadata)

    def read(self):

        return f"https://cw3e.ucsd.edu/images/CW3E_Obs/{self.watershed_location}_Latest_SurfaceMet.png"
