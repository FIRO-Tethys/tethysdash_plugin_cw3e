from datetime import datetime, timedelta, timezone
import re
import requests
from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin
from tethysapp.tethysdash.exceptions import VisualizationError

BASE_URL = "https://cw3e.ucsd.edu/images"

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

# plot_type display label -> v1 product plot token.
PLOT_TYPE_CODES = {
    "Probability": "probability",
    "Contours": "spaghetti",
}

# West-WRF (legacy, not run in real-time) plot_type -> legacy token, and the
# domains it supports (Northeast Pacific and U.S. West Coast only).
WEST_WRF_PLOT_TOKENS = {"Probability": "Prob", "Contours": "Spag"}
WEST_WRF_DOMAINS = {"Northeast Pacific", "U.S. West Coast"}


class IVTEnsembleProbability(TethysDashPlugin):
    name = "cw3e_ivt_ensemble_probability"
    tags = [
        "cw3e",
        "ar",
        "ivt",
        "gefs",
        "ecmwf",
        "probability",
    ]
    description = "Probability of IVT exceeding thresholds based on the forecast members and ensemble mean IVT vectors or ensemble member contours (thin lines) and ensemble mean (thick blue line). More information can be found at https://cw3e.ucsd.edu/iwv-and-ivt-forecasts/"
    args = {
        "date": "date",
        "model": ["GEFS", "ECMWF EPS", "West-WRF"],
        "threshold": ["IVT >250 kg/m/s", "IVT >500 kg/m/s", "IVT >750 kg/m/s"],
        "forecast_hour": list(range(0, 246, 6)),
        "domain": [
            "Northeast Pacific",
            "U.S. West Coast",
            "Interior West",
            "North America",
        ],
        "plot_type": ["Probability", "Contours"],
    }
    group = "CW3E"
    label = "IVT Ensemble Probabilities"
    type = "image"
    attribution = "CW3E"

    def run(self):
        threshold = int(re.search(r"\d+", self.threshold).group())
        region = DOMAIN_CODES[self.domain]

        # West-WRF has no v1 product (not run in real-time); use the legacy URL.
        # It only covers the Northeast Pacific and U.S. West Coast domains.
        if self.model == "West-WRF":
            if self.domain not in WEST_WRF_DOMAINS:
                raise VisualizationError(
                    "West-WRF IVT ensemble products are only available for the "
                    "Northeast Pacific and U.S. West Coast domains."
                )
            token = WEST_WRF_PLOT_TOKENS[self.plot_type]
            return (
                "https://cw3e.ucsd.edu/images/wwrf/ensemble/IVT_maps/"
                f"West-WRF_IVT{token}_{threshold}_{region}-F{int(self.forecast_hour)}.png"
            )

        model_info = MODELS[self.model]
        model = model_info["code"]
        interval = model_info["cycle_interval"]
        product = f"ivt{threshold}_{PLOT_TYPE_CODES[self.plot_type]}_map"
        forecast_hour = f"F{int(self.forecast_hour):03d}"

        if self.date == "latest":
            return self._resolve_latest_url(
                product, model, interval, region, forecast_hour
            )

        # Validate the requested run cycle for the selected model.
        if self.date.hour % interval != 0:
            valid = ", ".join(f"{h:02d}Z" for h in range(0, 24, interval))
            raise VisualizationError(
                f"{self.model} model runs are only available at {valid}."
            )

        date_str = self.date.strftime("%Y%m%d%H")
        return self._build_url(product, model, region, date_str, forecast_hour)

    def _build_url(self, product, model, region, date_str, forecast_hour):
        return (
            f"{BASE_URL}/{product}/v1/{model}/{region}/{date_str}/1/"
            f"{product}__v1__{model}__{region}__{date_str}__1__{forecast_hour}.png"
        )

    def _resolve_latest_url(self, product, model, interval, region, forecast_hour):
        """Probe model run cycles backwards to find the newest available run."""
        # Round the current time down to the nearest valid run cycle.
        now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
        cycle = now.replace(hour=(now.hour // interval) * interval)

        # Look back up to ~10 days worth of run cycles.
        for _ in range((10 * 24) // interval):
            date_str = cycle.strftime("%Y%m%d%H")
            url = self._build_url(product, model, region, date_str, forecast_hour)
            try:
                if requests.head(url, timeout=10).status_code == 200:
                    return url
            except requests.RequestException:
                # Site unreachable (e.g. a blocked IP); assume the most
                # recent cycle's image exists instead of probing every cycle.
                return url
            cycle -= timedelta(hours=interval)

        raise VisualizationError(
            f"No IVT ensemble image found for {self.model} "
            f"({region}, {forecast_hour}) in the last 10 days."
        )
