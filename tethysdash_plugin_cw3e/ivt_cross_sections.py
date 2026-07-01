from datetime import datetime, timedelta, timezone
import requests
from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin
from tethysapp.tethysdash.exceptions import VisualizationError

BASE_URL = "https://cw3e.ucsd.edu/images/ivt_crosssection/v1"

# model display label -> v1 model path code and run-cycle interval (hours).
# GFS runs every 6 hours (00/06/12/18Z); ECMWF runs only at 00Z and 12Z.
MODELS = {
    "GFS": {"code": "GFS_25", "cycle_interval": 6},
    "ECMWF": {"code": "ECMWF_HRes", "cycle_interval": 12},
}


class IVTCrossSections(TethysDashPlugin):
    name = "cw3e_ivt_cross_sections"
    tags = [
        "cw3e",
        "cross",
        "sections",
        "ivt",
    ]
    description = "Cross sections that illustrate the forecasted conditions along a longitudinal line from 25-65°N for the given forecast time from the GFS or ECMWF deterministic model.  More information can be found at https://cw3e.ucsd.edu/iwv-and-ivt-forecasts/"
    args = {
        "date": "date",
        "model": ["GFS", "ECMWF"],
        "longitude": [
            {"value": lon, "label": f"{lon} W"} for lon in range(105, 180, 5)
        ],
        "forecast_hour": [
            {"value": f"{hour:03}", "label": hour} for hour in range(0, 132, 12)
        ],
    }
    group = "CW3E"
    label = "IVT Cross Sections"
    type = "image"
    attribution = "CW3E"

    def run(self):
        model_info = MODELS[self.model]
        model = model_info["code"]
        interval = model_info["cycle_interval"]
        location = f"25-65N_{self.longitude}W"
        forecast_hour = f"F{self.forecast_hour}"

        if self.date == "latest":
            return self._resolve_latest_url(model, interval, location, forecast_hour)

        # Validate the requested run cycle for the selected model.
        if self.date.hour % interval != 0:
            valid = ", ".join(f"{h:02d}Z" for h in range(0, 24, interval))
            raise VisualizationError(
                f"{self.model} model runs are only available at {valid}."
            )

        date_str = self.date.strftime("%Y%m%d%H")
        return self._build_url(model, location, date_str, forecast_hour)

    def _build_url(self, model, location, date_str, forecast_hour):
        return (
            f"{BASE_URL}/{model}/{location}/{date_str}/1/"
            f"ivt_crosssection__v1__{model}__{location}__{date_str}__1__{forecast_hour}.png"
        )

    def _resolve_latest_url(self, model, interval, location, forecast_hour):
        """Probe model run cycles backwards to find the newest available run."""
        # Round the current time down to the nearest valid run cycle.
        now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
        cycle = now.replace(hour=(now.hour // interval) * interval)

        # Look back up to ~10 days worth of run cycles.
        for _ in range((10 * 24) // interval):
            date_str = cycle.strftime("%Y%m%d%H")
            url = self._build_url(model, location, date_str, forecast_hour)
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
            f"No IVT cross section image found for {self.model} "
            f"({location}, {forecast_hour}) in the last 10 days."
        )
