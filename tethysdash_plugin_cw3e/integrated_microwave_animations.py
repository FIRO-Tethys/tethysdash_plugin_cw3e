from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin
from .constants import SurfaceMeterologyLocations


class IntegratedMicrowaveAnimations(TethysDashPlugin):
    name = "cimss_integrated_microwave_animations"
    tags = [
        "cw3e",
        "wisconsion",
        "cimss",
        "morphed",
        "integrated",
        "microwave",
        "precipitation",
        "water vapor",
        "animation",
    ]
    description = "Animated depiction of the total precipitable water from Morphed Integrated Microwave Imagery at CIMSS (University of Wisconsin). More information can be found at https://cw3e.ucsd.edu/satellite/#ARD."
    args = {
        "domain": ["Global", "NE Pacific", "N Atlantic"],
    }
    group = "CIMSS"
    label = "Integrated Microwave Animations of Integrated Water Vapor"
    type = "image"
    attribution = "CW3E"

    def run(self):
        if self.domain == "Global":
            return "https://cw3e.ucsd.edu/images/ssmi/download/images/Global/GlobalAnim.gif"

        if self.domain == "NE Pacific":
            return (
                "https://cw3e.ucsd.edu/images/ssmi/download/images/NEPac/NEPacAnim.gif"
            )

        if self.domain == "N Atlantic":
            return "https://cw3e.ucsd.edu/images/ssmi/download/images/NAtl/NAtlAnim.gif"
