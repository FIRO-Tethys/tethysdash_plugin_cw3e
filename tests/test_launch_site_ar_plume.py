import pytest
from tethysapp.tethysdash.exceptions import VisualizationError

from tethysdash_plugin_cw3e.ar_scale_plume_diagrams import ARScalePlumeDiagrams
from tethysdash_plugin_cw3e.launch_site_ar_plume import LaunchSiteARScalePlume
from tethysdash_plugin_cw3e.radiosonde_sites import LAUNCH_SITES

OPTIONS = {
    "plot_type": "AR Scale",
    "model": "U.S. National Model (GEFS)",
    "AR_scale_calculated_by": "Ensemble Mean",
    "date": "2026-11-24T00:00",
}


@pytest.mark.parametrize("site", LAUNCH_SITES.values(), ids=lambda s: s.code)
def test_shows_the_plume_at_the_sites_registry_point(site):
    url = LaunchSiteARScalePlume(site=site.code, **OPTIONS).run()

    assert url == ARScalePlumeDiagrams(
        transect_location=site.ar_transect,
        **{"transect_location.location": site.ar_location},
        **OPTIONS,
    ).run()


def test_url_names_the_site_point():
    url = LaunchSiteARScalePlume(site="USTAC", **OPTIONS).run()

    assert "/GEFS_50/foothills_47.0N_122.0W/2026112400/" in url


def test_west_wrf_uses_its_legacy_url():
    options = {**OPTIONS, "model": "West-WRF"}

    url = LaunchSiteARScalePlume(site="USBOD", **options).run()

    assert url.startswith("https://cw3e.ucsd.edu/images/wwrf/")


def test_unknown_site_raises():
    with pytest.raises(VisualizationError, match="Unknown launch site"):
        LaunchSiteARScalePlume(site="USXXX", **OPTIONS).run()
