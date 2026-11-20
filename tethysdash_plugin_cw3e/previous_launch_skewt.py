"""Skew-T of the most recent CW3E radiosonde launch at a launch site.

CW3E lists every launch per site in CW3E_Obs_Radiosondes_Launches.json, as
{site code: ["YYYYMMDDHHMM", ...]} in time order, and publishes a skew-T image
per launch.
"""

import requests
from tethysapp.tethysdash.exceptions import VisualizationError
from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin

from .radiosonde_sites import SITE_ARG, get_launch_site

LAUNCHES_URL = (
    "https://cw3e.ucsd.edu/images/json/CW3E_Obs_Radiosondes_Launches.json"
)
SKEWT_BASE_URL = "https://cw3e.ucsd.edu/images/radiosonde_skewts/v1/cw3e"
# The newest launch's image can lag the launch list; look this far back.
LAUNCHES_TO_TRY = 5


def skewt_url(site_code, launch):
    """Skew-T image URL for a launch time such as "202611022256"."""
    return (
        f"{SKEWT_BASE_URL}/{site_code}/{launch}/1/"
        f"radiosonde_skewts__v1__cw3e__{site_code}__{launch}__1__.png"
    )


def fetch_launches():
    """Return CW3E's launch list, {site code: [launch times]}."""
    response = requests.get(LAUNCHES_URL, timeout=(5, 20))
    response.raise_for_status()
    return response.json()


def image_exists(url):
    return requests.head(url, timeout=(3, 5)).status_code == 200


class PreviousLaunchSkewT(TethysDashPlugin):
    name = "cw3e_previous_launch_skewt"
    tags = ["cw3e", "radiosonde", "skew-t", "sounding", "launch"]
    description = (
        "Skew-T diagram from the most recent CW3E radiosonde launch at a "
        "launch site. More information can be found at "
        "https://cw3e.ucsd.edu/cw3e_observations_radiosondes/"
    )
    args = {"site": SITE_ARG}
    group = "CW3E"
    label = "Previous Launch Skew-T"
    type = "image"
    attribution = "CW3E"

    def run(self):
        site = get_launch_site(self.site)
        try:
            launches = fetch_launches().get(site.code, [])
        except (requests.RequestException, ValueError) as error:
            raise VisualizationError(
                f"Could not read the CW3E launch list ({type(error).__name__})."
            )
        if not launches:
            raise VisualizationError(f"{site.label} has no launches yet.")

        recent = sorted(launches, reverse=True)[:LAUNCHES_TO_TRY]
        for launch in recent:
            url = skewt_url(site.code, launch)
            try:
                if image_exists(url):
                    return url
            except requests.RequestException:
                # Image server unreachable from here (e.g. a blocked IP);
                # the browser may still reach it, so show the newest launch.
                return skewt_url(site.code, recent[0])

        raise VisualizationError(
            f"No skew-T image found for the last {len(recent)} launches at "
            f"{site.label}."
        )
