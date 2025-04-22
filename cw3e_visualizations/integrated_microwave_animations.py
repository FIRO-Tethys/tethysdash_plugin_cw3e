from intake.source import base
from .constants import SurfaceMeterologyLocations


class IntegratedMicrowaveAnimations(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "cw3e_integrated_microwave_animations"
    visualization_args = {
        "domain": ["Global", "NE Pacific", "N Atlantic"],
    }
    visualization_group = "CW3E"
    visualization_label = "Integrated Microwave Animations of Integrated Water Vapor"
    visualization_type = "image"

    def __init__(self, domain, metadata=None):
        # store important kwargs
        self.domain = domain
        super(IntegratedMicrowaveAnimations, self).__init__(metadata=metadata)

    def read(self):
        if self.domain == "Global":
            return "https://cw3e.ucsd.edu/images/ssmi/download/images/Global/GlobalAnim.gif"

        if self.domain == "NE Pacific":
            return (
                "https://cw3e.ucsd.edu/images/ssmi/download/images/NEPac/NEPacAnim.gif"
            )

        if self.domain == "N Atlantic":
            return "https://cw3e.ucsd.edu/images/ssmi/download/images/NAtl/NAtlAnim.gif"
