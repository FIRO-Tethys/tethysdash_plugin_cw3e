"""Latest surface observations at a radiosonde launch site, from Synoptic.

Shows the values entered into the MW51 before a launch: station pressure (hPa),
temperature (C), relative humidity (%), wind direction (deg) and wind speed
(m/s). The Synoptic API token is read from the SYNOPTIC_TOKEN environment
variable of the Tethys server.
"""

import os
from datetime import datetime, timezone

import requests
from tethysapp.tethysdash.exceptions import VisualizationError
from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin

from .radiosonde_sites import SITE_ARG, get_launch_site

LATEST_URL = "https://api.synopticdata.com/v2/stations/latest"
TOKEN_VARIABLE = "SYNOPTIC_TOKEN"
# Observations older than this are ignored, so a site falls back to its next
# station rather than showing hours-old conditions.
WITHIN_MINUTES = 180

# (Synoptic variable, card label, unit, decimals, card icon, card color)
MEASUREMENTS = (
    ("pressure", "Pressure", "hPa", 1, "BiTachometer", "#6f42c1"),
    ("air_temp", "Temperature", "°C", 1, "BiSolidThermometer", "#dc3545"),
    ("relative_humidity", "Relative humidity", "%", 0, "BiDroplet", "#0d6efd"),
    ("wind_direction", "Wind direction", "°", 0, "BiCompass", "#198754"),
    ("wind_speed", "Wind speed", "m/s", 1, "BiWind", "#20c997"),
)


def fetch_latest(station, token):
    """Return Synoptic's latest-observation response for one station."""
    params = {
        "token": token,
        "stid": station,
        "vars": ",".join(m[0] for m in MEASUREMENTS),
        "units": "metric,pres|mb",
        "within": WITHIN_MINUTES,
        "obtimezone": "utc",
    }
    response = requests.get(LATEST_URL, params=params, timeout=(5, 20))
    return response.json()


def latest_values(response):
    """Map each variable to its newest (value, observed time) in a response.

    Synoptic names observations "<variable>_value_<n>", with a trailing "d"
    when the value is derived (station pressure from the altimeter setting,
    for instance). Variables the station did not report are left out.
    """
    stations = response.get("STATION") or []
    observations = stations[0].get("OBSERVATIONS", {}) if stations else {}
    values = {}
    for variable, *_ in MEASUREMENTS:
        candidates = [
            (_parse_time(obs["date_time"]), obs["value"])
            for key, obs in observations.items()
            if key.startswith(f"{variable}_value_")
            and isinstance(obs, dict)
            and obs.get("value") is not None
        ]
        if candidates:
            observed, value = max(candidates, key=lambda c: c[0])
            values[variable] = (value, observed)
    return values


def _parse_time(text):
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def _format_age(observed, now):
    minutes = int((now - observed).total_seconds() // 60)
    if minutes < 60:
        return f"{minutes} min ago"
    return f"{minutes // 60} h {minutes % 60} min ago"


class SynopticSurfaceConditions(TethysDashPlugin):
    name = "cw3e_synoptic_surface_conditions"
    tags = ["cw3e", "radiosonde", "synoptic", "surface", "mw51"]
    description = (
        "Latest surface pressure, temperature, relative humidity and wind at "
        "a CW3E radiosonde launch site, from Synoptic, for entry into the "
        "MW51 before a launch."
    )
    args = {"site": SITE_ARG}
    group = "CW3E"
    label = "Launch Site Surface Conditions"
    type = "card"
    attribution = "Synoptic Data PBC"

    def run(self):
        site = get_launch_site(self.site)
        token = os.environ.get(TOKEN_VARIABLE)
        if not token:
            raise VisualizationError(
                f"No Synoptic API token. Set {TOKEN_VARIABLE} on the server."
            )

        unavailable = []
        for station in site.surface_stations:
            try:
                response = fetch_latest(station, token)
            except (requests.RequestException, ValueError) as error:
                # Only the error type: requests messages include the URL,
                # and with it the token.
                unavailable.append(f"{station} ({type(error).__name__})")
                continue
            summary = response.get("SUMMARY", {})
            values = latest_values(response)
            if summary.get("RESPONSE_CODE") == 1 and values:
                return self._card(site, station, values, unavailable)
            message = summary.get("RESPONSE_MESSAGE") or "no observations"
            unavailable.append(f"{station} ({message})")

        raise VisualizationError(
            f"No surface observations for {site.label} in the last "
            f"{WITHIN_MINUTES // 60} hours: {'; '.join(unavailable)}"
        )

    def _card(self, site, station, values, unavailable):
        data = []
        for variable, label, unit, decimals, icon, color in MEASUREMENTS:
            if variable in values:
                value = f"{values[variable][0]:.{decimals}f} {unit}"
            else:
                value = "Not reported"
            data.append(
                {"label": label, "value": value, "icon": icon, "color": color}
            )

        oldest = min(observed for _, observed in values.values())
        now = datetime.now(timezone.utc)
        description = (
            f"Station {station}, observed {oldest:%Y-%m-%d %H:%M} UTC "
            f"({_format_age(oldest, now)})"
        )
        if unavailable:
            description += f". Unavailable: {', '.join(unavailable)}"
        return {
            "title": f"{site.label} surface conditions",
            "description": description,
            "data": data,
        }
