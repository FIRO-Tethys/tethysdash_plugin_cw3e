import pytest
import requests
from tethysapp.tethysdash.exceptions import VisualizationError

from tethysdash_plugin_cw3e import previous_launch_skewt as skewt
from tethysdash_plugin_cw3e.previous_launch_skewt import (
    PreviousLaunchSkewT,
    skewt_url,
)


def run_for(site, monkeypatch, launches, published=None, head_error=None):
    """Run the plugin with the launch list and image checks stubbed.

    published: launch times whose image exists (default: all of them).
    """
    checked = []

    def fake_exists(url):
        checked.append(url)
        if head_error:
            raise head_error
        return published is None or any(t in url for t in published)

    monkeypatch.setattr(skewt, "fetch_launches", lambda: launches)
    monkeypatch.setattr(skewt, "image_exists", fake_exists)
    return PreviousLaunchSkewT(site=site).run(), checked


def test_skewt_url_matches_cw3e_layout():
    assert skewt_url("USSIO", "202611022256") == (
        "https://cw3e.ucsd.edu/images/radiosonde_skewts/v1/cw3e/USSIO/"
        "202611022256/1/radiosonde_skewts__v1__cw3e__USSIO__202611022256__1__.png"
    )


def test_returns_the_most_recent_launch(monkeypatch):
    launches = {"USSIO": ["202611010000", "202611022256", "202611022100"]}

    url, checked = run_for("USSIO", monkeypatch, launches)

    assert url == skewt_url("USSIO", "202611022256")
    assert checked == [url]


def test_falls_back_when_the_newest_image_is_not_published(monkeypatch):
    launches = {"USSIO": ["202611022100", "202611022256"]}

    url, _ = run_for(
        "USSIO", monkeypatch, launches, published={"202611022100"}
    )

    assert url == skewt_url("USSIO", "202611022100")


def test_unreachable_image_server_returns_the_newest_launch(monkeypatch):
    launches = {"USSIO": ["202611022100", "202611022256"]}

    url, _ = run_for(
        "USSIO", monkeypatch, launches, head_error=requests.ConnectTimeout()
    )

    assert url == skewt_url("USSIO", "202611022256")


def test_site_without_launches_raises(monkeypatch):
    with pytest.raises(VisualizationError, match="USSHC .* has no launches"):
        run_for("USSHC", monkeypatch, {"USSHC": []})


def test_no_published_image_in_recent_launches_raises(monkeypatch):
    launches = {"USGHC": [f"2026031{d}0000" for d in range(10)]}

    with pytest.raises(VisualizationError, match="last 5 launches"):
        run_for("USGHC", monkeypatch, launches, published=set())


def test_unreadable_launch_list_raises(monkeypatch):
    def broken():
        raise requests.HTTPError("503")

    monkeypatch.setattr(skewt, "fetch_launches", broken)

    with pytest.raises(VisualizationError, match="HTTPError"):
        PreviousLaunchSkewT(site="USSIO").run()
