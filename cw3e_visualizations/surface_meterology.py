from intake.source import base
from .constants import SurfaceMeterologyLocations


class SurfaceMeterology(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "cw3e_surface_meterology"
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
