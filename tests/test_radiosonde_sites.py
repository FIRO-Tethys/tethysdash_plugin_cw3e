import math

import pytest
from tethysapp.tethysdash.exceptions import VisualizationError

from tethysdash_plugin_cw3e.ar_scale_plume_diagrams import ARScalePlumeDiagrams
from tethysdash_plugin_cw3e.radiosonde_sites import (
    LAUNCH_SITES,
    SITE_ARG,
    get_launch_site,
)

SITES = list(LAUNCH_SITES.values())


def ar_plume_locations(transect):
    """Location values the AR Scale plume plugin offers for a transect."""
    for option in ARScalePlumeDiagrams.args["transect_location"]:
        if option["value"] == transect:
            return {loc["value"] for loc in option["sub_args"]["location"]}
    return set()


def distance_km(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, (lat1, lon1, lat2, lon2))
    h = (
        math.sin((lat2 - lat1) / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    )
    return 6371 * 2 * math.asin(math.sqrt(h))


def test_registry_has_the_eight_cw3e_launch_sites():
    assert list(LAUNCH_SITES) == [
        "USSIO", "USCAT", "USSOD", "USBOD", "USYUB", "USSHC", "USTAC", "USGHC",
    ]


@pytest.mark.parametrize("site", SITES, ids=lambda s: s.code)
def test_ar_location_is_offered_by_the_plume_plugin(site):
    assert site.ar_location in ar_plume_locations(site.ar_transect)


@pytest.mark.parametrize("site", SITES, ids=lambda s: s.code)
def test_ar_location_is_near_the_site(site):
    lat, lon360 = map(float, site.ar_location.split("_"))

    km = distance_km(site.latitude, site.longitude, lat, lon360 - 360)

    assert km < 75


@pytest.mark.parametrize("site", SITES, ids=lambda s: s.code)
def test_site_lists_at_least_one_surface_station(site):
    assert site.surface_stations


def test_site_arg_matches_registry_order_and_labels():
    assert SITE_ARG == [
        {"value": site.code, "label": f"{site.code} - {site.name}"}
        for site in SITES
    ]


def test_get_launch_site_returns_the_site():
    assert get_launch_site("USSHC").surface_stations == ("WXM3988", "KRDD")


def test_get_launch_site_rejects_unknown_code():
    with pytest.raises(VisualizationError, match="Unknown launch site 'USXXX'"):
        get_launch_site("USXXX")
