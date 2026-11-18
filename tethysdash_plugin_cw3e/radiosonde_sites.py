"""Radiosonde launch sites shared by the CW3E launch dashboard plugins.

Site names and coordinates come from CW3E's radiosonde site list,
https://cw3e.ucsd.edu/images/json/CW3E_Obs_Radiosondes.json. The surface
stations are the ones CW3E picked for each launch site (November 2026); a site
lists a fallback after its preferred station when the preferred one may not be
reachable. The AR point is the nearest point on the closest transect of the
AR Scale plume diagrams (see ar_scale_plume_diagrams.py), in that plugin's
"<lat>_<lon 0-360>" form.
"""

from dataclasses import dataclass

from tethysapp.tethysdash.exceptions import VisualizationError


@dataclass(frozen=True)
class LaunchSite:
    code: str
    name: str
    latitude: float
    longitude: float
    surface_stations: tuple
    ar_transect: str
    ar_location: str

    @property
    def label(self):
        return f"{self.code} - {self.name}"


_SITES = (
    LaunchSite(
        "USSIO", "Scripps Pier, CA", 32.8664, -117.2553,
        ("C3SIO",), "coast", "33.0_242.5",
    ),
    LaunchSite(
        "USCAT", "Catalina Island, CA", 33.44617, -118.48276,
        ("C3CAT",), "coast", "34.0_241.5",
    ),
    # CW3E lists Seven Oaks Dam only to 0.1 degree.
    LaunchSite(
        "USSOD", "Seven Oaks Dam, CA", 34.1, -117.1,
        ("C3SOD",), "foothills", "34.0_242.5",
    ),
    LaunchSite(
        "USBOD", "Bodega Bay, CA", 38.318629, -123.071526,
        ("C3BBY",), "coast", "38.5_237.0",
    ),
    LaunchSite(
        "USYUB", "Marysville, CA", 39.20201, -121.519731,
        ("C3BVS",), "foothills", "39.0_239.0",
    ),
    # WXM3988 is a private Weather XM station; KRDD (Redding airport) is the
    # alternative CW3E named if it is not accessible.
    LaunchSite(
        "USSHC", "Shasta College, CA", 40.62, -122.32,
        ("WXM3988", "KRDD"), "foothills", "40.5_238.0",
    ),
    LaunchSite(
        "USTAC", "Tacoma, WA", 47.13378, -122.2569,
        ("KTCM",), "foothills", "47.0_238.0",
    ),
    LaunchSite(
        "USGHC", "Grays Harbor College, WA", 46.955, -123.80157,
        ("KHQM",), "coast", "47.0_236.0",
    ),
)

LAUNCH_SITES = {site.code: site for site in _SITES}

# Dropdown arg for plugins that take a launch site, e.g. {"site": SITE_ARG}.
SITE_ARG = [{"value": site.code, "label": site.label} for site in _SITES]


def get_launch_site(code):
    """Return the LaunchSite for a site code such as "USSIO"."""
    try:
        return LAUNCH_SITES[code]
    except KeyError:
        raise VisualizationError(
            f"Unknown launch site '{code}'. "
            f"Expected one of: {', '.join(LAUNCH_SITES)}"
        )
