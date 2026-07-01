from datetime import datetime, timedelta, timezone
import requests
from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin
from tethysapp.tethysdash.exceptions import VisualizationError

BASE_URL = "https://cw3e.ucsd.edu/images/250hpa_wind_map/v1"

# model display label -> v1 model path code and run-cycle interval (hours).
# GFS runs every 6 hours (00/06/12/18Z); ECMWF runs only at 00Z and 12Z.
MODELS = {
    "GFS": {"code": "GFS_25", "cycle_interval": 6},
    "ECMWF": {"code": "ECMWF_HRes", "cycle_interval": 12},
}

# Both models produce forecasts every 3 hours.
FORECAST_INTERVAL_HOURS = 3


class Winds250hPA(TethysDashPlugin):
    name = "cw3e_250_hpa_winds"
    tags = [
        "cw3e",
        "gfs",
        "ecmwf",
        "winds",
    ]
    description = "250-hPa wind barbs with magnitude shaded in knots and heights contoured in geopotential meters from the Global Forecast System (GFS) and the European Centre for Medium-Range Weather Forecasts (ECMWF). More information can be found at https://cw3e.ucsd.edu/250Winds_NPac/"
    args = {
        "date": "date",
        "model": ["GFS", "ECMWF"],
        "forecast_hour": "number",
        "region": [
            {"value": "NPac", "label": "North Pacific"},
            {"value": "NEPac", "label": "Northeast Pacific"},
            {"value": "USWC", "label": "U.S. West Coast"},
            {"value": "NAmerica", "label": "North America"},
        ],
    }
    group = "CW3E"
    label = "250-hPa Winds and Height Model Analysis and Forecasts"
    type = "image"
    loading_icon = False
    attribution = "CW3E"

    def run(self):
        model_info = MODELS[self.model]
        model = model_info["code"]
        interval = model_info["cycle_interval"]
        region = self.region
        forecast_hour = self._format_forecast_hour()

        if self.date == "latest":
            return self._resolve_latest_url(model, interval, region, forecast_hour)

        # Validate the requested run cycle for the selected model.
        if self.date.hour % interval != 0:
            valid = ", ".join(f"{h:02d}Z" for h in range(0, 24, interval))
            raise VisualizationError(
                f"{self.model} model runs are only available at {valid}."
            )

        date_str = self.date.strftime("%Y%m%d%H")
        return self._build_url(model, region, date_str, forecast_hour)

    def _format_forecast_hour(self):
        """Normalize and validate the user-entered forecast hour."""
        try:
            hour = int(float(str(self.forecast_hour).lstrip("Ff")))
        except (TypeError, ValueError):
            raise VisualizationError(
                f"Invalid forecast hour: {self.forecast_hour!r}. "
                "Enter a number of hours, e.g. 0, 3, or 120."
            )
        if hour < 0 or hour % FORECAST_INTERVAL_HOURS != 0:
            raise VisualizationError(
                f"Forecasts are only available every {FORECAST_INTERVAL_HOURS} "
                f"hours (0, 3, 6, ...); {hour} is not valid."
            )
        return f"F{hour:03d}"

    def _build_url(self, model, region, date_str, forecast_hour):
        return (
            f"{BASE_URL}/{model}/{region}/{date_str}/1/"
            f"250hpa_wind_map__v1__{model}__{region}__{date_str}__1__{forecast_hour}.png"
        )

    def _resolve_latest_url(self, model, interval, region, forecast_hour):
        """Probe model run cycles backwards to find the newest available run."""
        # Round the current time down to the nearest valid run cycle.
        now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
        cycle = now.replace(hour=(now.hour // interval) * interval)

        # Look back up to ~10 days worth of run cycles.
        for _ in range((10 * 24) // interval):
            date_str = cycle.strftime("%Y%m%d%H")
            url = self._build_url(model, region, date_str, forecast_hour)
            try:
                if requests.head(url, timeout=10).status_code == 200:
                    return url
            except requests.RequestException:
                # Site unreachable (e.g. a blocked IP). CW3E products lag
                # their synoptic cycle by several hours, so fall back to
                # the newest cycle ~12h old (which has realistically
                # finished) instead of the current one, which usually is
                # not published yet. Rounded to the model's cycle step.
                fallback = now - timedelta(hours=12)
                fallback_str = fallback.replace(
                    hour=(fallback.hour // interval) * interval,
                    minute=0,
                    second=0,
                    microsecond=0,
                ).strftime("%Y%m%d%H")
                return url.replace(date_str, fallback_str)
            cycle -= timedelta(hours=interval)

        raise VisualizationError(
            f"No 250-hPa wind image found for {self.model} "
            f"({region}, {forecast_hour}) in the last 10 days."
        )
