from datetime import datetime, timedelta, timezone
import requests
from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin
from tethysapp.tethysdash.exceptions import VisualizationError

BASE_URL = "https://cw3e.ucsd.edu/images/ivt_thumbnail_maps/v1"

# model display label -> v1 model path code and run-cycle interval (hours).
# GEFS runs every 6 hours (00/06/12/18Z); ECMWF runs only at 00Z and 12Z.
MODELS = {
    "GEFS": {"code": "GEFS_50", "cycle_interval": 6},
    "ECMWF EPS": {"code": "ECMWF_ENS", "cycle_interval": 12},
}

# domain display label -> v1 region path component.
DOMAIN_CODES = {
    "Northeast Pacific": "NEPac",
    "U.S. West Coast": "USWC",
    "Interior West": "IntWest",
    "North America": "NAmerica",
}


class IVTThumbnailEnsembles(TethysDashPlugin):
    name = "cw3e_ivt_thumbnail_ensembles"
    tags = [
        "cw3e",
        "ar",
        "ivt",
        "gefs",
        "ecmwf",
        "thumbnails",
    ]
    description = "Collection of thumbnails depicting IVT exceeding thresholds for each ensemble. More information can be found at https://cw3e.ucsd.edu/iwv-and-ivt-forecasts/"
    args = {
        "date": "date",
        "model": ["GEFS", "ECMWF EPS"],
        "forecast_hour": list(range(0, 366, 12)),
        "domain": [
            "Northeast Pacific",
            "U.S. West Coast",
            "Interior West",
            "North America",
        ],
    }
    group = "CW3E"
    label = "IVT Thumbnail Ensembles"
    type = "image"
    attribution = "CW3E"

    def run(self):
        model_info = MODELS[self.model]
        model = model_info["code"]
        interval = model_info["cycle_interval"]
        region = DOMAIN_CODES[self.domain]
        forecast_hour = f"F{int(self.forecast_hour):03d}"

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

    def _build_url(self, model, region, date_str, forecast_hour):
        return (
            f"{BASE_URL}/{model}/{region}/{date_str}/1/"
            f"ivt_thumbnail_maps__v1__{model}__{region}__{date_str}__1__{forecast_hour}.png"
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
                pass
            cycle -= timedelta(hours=interval)

        raise VisualizationError(
            f"No IVT thumbnail image found for {self.model} "
            f"({region}, {forecast_hour}) in the last 10 days."
        )
