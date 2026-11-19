from datetime import datetime, timezone

import pytest
import requests
from tethysapp.tethysdash.exceptions import VisualizationError

from tethysdash_plugin_cw3e import synoptic_surface_conditions as synoptic
from tethysdash_plugin_cw3e.synoptic_surface_conditions import (
    SynopticSurfaceConditions,
    latest_values,
)

TOKEN = "test-token-123"


def obs(value, time="2026-11-18T20:50:00Z"):
    return {"value": value, "date_time": time}


def response(observations=None, code=1, message="OK"):
    """A Synoptic latest-observation response for one station."""
    body = {"SUMMARY": {"RESPONSE_CODE": code, "RESPONSE_MESSAGE": message}}
    if observations is not None:
        body["STATION"] = [{"STID": "X", "OBSERVATIONS": observations}]
    return body


FULL = {
    "pressure_value_1d": obs(1012.34),
    "air_temp_value_1": obs(15.26),
    "relative_humidity_value_1": obs(81.6),
    "wind_direction_value_1": obs(270.0),
    "wind_speed_value_1": obs(0.0),
}


def card_for(site, monkeypatch, responses):
    """Run the plugin with fetch_latest stubbed by station."""
    monkeypatch.setenv("SYNOPTIC_TOKEN", TOKEN)
    calls = []

    def fake_fetch(station, token):
        calls.append(station)
        result = responses[station]
        if isinstance(result, Exception):
            raise result
        return result

    monkeypatch.setattr(synoptic, "fetch_latest", fake_fetch)
    return SynopticSurfaceConditions(site=site).run(), calls


def values_by_label(card):
    return {item["label"]: item["value"] for item in card["data"]}


def test_latest_values_takes_the_newest_of_measured_and_derived():
    observations = {
        "pressure_value_1": obs(1000.0, "2026-11-18T19:00:00Z"),
        "pressure_value_1d": obs(1001.0, "2026-11-18T20:00:00Z"),
    }

    values = latest_values(response(observations))

    assert values == {
        "pressure": (1001.0, datetime(2026, 11, 18, 20, tzinfo=timezone.utc)),
    }


def test_latest_values_skips_missing_values_and_empty_responses():
    assert latest_values(response({"air_temp_value_1": obs(None)})) == {}
    assert latest_values(response()) == {}


def test_card_shows_the_five_mw51_values_with_units(monkeypatch):
    card, calls = card_for("USSIO", monkeypatch, {"C3SIO": response(FULL)})

    assert calls == ["C3SIO"]
    assert card["title"] == "USSIO - Scripps Pier, CA surface conditions"
    assert values_by_label(card) == {
        "Pressure": "1012.3 hPa",
        "Temperature": "15.3 °C",
        "Relative humidity": "82 %",
        "Wind direction": "270 °",
        "Wind speed": "0.0 m/s",
    }
    assert card["description"].startswith(
        "Station C3SIO, observed 2026-11-18 20:50 UTC ("
    )


def test_card_marks_variables_the_station_did_not_report(monkeypatch):
    partial = {"air_temp_value_1": obs(9.0)}

    card, _ = card_for("USSIO", monkeypatch, {"C3SIO": response(partial)})

    assert values_by_label(card)["Pressure"] == "Not reported"
    assert values_by_label(card)["Temperature"] == "9.0 °C"


def test_falls_back_to_the_next_station(monkeypatch):
    card, calls = card_for(
        "USSHC",
        monkeypatch,
        {
            "WXM3988": response(code=200, message="Authentication failure"),
            "KRDD": response(FULL),
        },
    )

    assert calls == ["WXM3988", "KRDD"]
    assert card["description"].startswith("Station KRDD,")
    assert card["description"].endswith(
        "Unavailable: WXM3988 (Authentication failure)"
    )


def test_network_errors_do_not_reveal_the_token(monkeypatch):
    error = requests.ConnectionError(f"failed: /latest?token={TOKEN}")

    card, _ = card_for(
        "USSHC", monkeypatch, {"WXM3988": error, "KRDD": response(FULL)}
    )

    assert card["description"].endswith("Unavailable: WXM3988 (ConnectionError)")
    assert TOKEN not in card["description"]


def test_no_station_with_data_raises(monkeypatch):
    with pytest.raises(VisualizationError, match=r"C3SIO \(Zero Results\)"):
        card_for(
            "USSIO",
            monkeypatch,
            {"C3SIO": response(code=2, message="Zero Results")},
        )


def test_missing_token_raises(monkeypatch):
    monkeypatch.delenv("SYNOPTIC_TOKEN", raising=False)

    with pytest.raises(VisualizationError, match="SYNOPTIC_TOKEN"):
        SynopticSurfaceConditions(site="USSIO").run()
