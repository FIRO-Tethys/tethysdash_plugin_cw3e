from datetime import datetime, timedelta, timezone
import requests
from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin
from tethysapp.tethysdash.exceptions import VisualizationError

BASE_URL = "https://cw3e.ucsd.edu/images"

# model display label -> v1 model path code and run-cycle interval (hours).
# GEFS runs every 6 hours (00/06/12/18Z); ECMWF runs only at 00Z and 12Z.
MODELS = {
    "U.S. National Model (GEFS)": {"code": "GEFS_50", "cycle_interval": 6},
    "European Model (ECMWF)": {"code": "ECMWF_ENS", "cycle_interval": 12},
}

# plot_type display label -> v1 product plot token.
PLOT_CODES = {
    "Observed": "analysis",
    "Control Forecast": "control",
    "Ensemble Mean": "mean",
}

# Precipitation token used when show_precipitation is enabled: observed maps use
# QPE (estimate), forecast maps use QPF (forecast). Omitted when disabled.
PRECIP_TOKENS = {
    "Observed": "qpe_",
    "Control Forecast": "qpf_",
    "Ensemble Mean": "qpf_",
}

# location display label -> v1 location path component.
LOCATION_CODES = {
    "Coastal": "coast",
    "Foothills": "foothills",
    "Inland": "inland",
    "Interior West": "intwest",
}


class CoastalMaximumARScaleAndPrecipMaps(TethysDashPlugin):
    name = "cw3e_coastal_maximum_ar_scale_and_precip_maps"
    tags = [
        "cw3e",
        "ar",
        "landfall",
        "frequency",
        "probability",
        "coastal",
        "precipitation",
    ]
    description = "Represent the AR scale observed and forecast at each grid point. GEFS plots update about every six hours and ECMWF plots update about every 12 hours.. More information can be found at https://cw3e.ucsd.edu/arscale/"
    args = {
        "date": "date",
        "plot_type": ["Observed", "Control Forecast", "Ensemble Mean"],
        "show_precipitation": "checkbox",
        "model": [
            "European Model (ECMWF)",
            "U.S. National Model (GEFS)",
            "West-WRF",
        ],
        "location": ["Coastal", "Foothills", "Inland", "Interior West"],
    }
    group = "CW3E"
    label = "Coastal Maximum AR Scale and Precipitation Maps"
    type = "image"
    attribution = "CW3E"

    def run(self):
        # West-WRF has no v1 product (not run in real-time). It only provides the
        # forecast control and ensemble-mean maps (no observed, precip, or
        # per-location variants), so use the legacy URL for those two plot types.
        if self.model == "West-WRF":
            if self.plot_type == "Control Forecast":
                suffix = "Forecast"
            elif self.plot_type == "Ensemble Mean":
                suffix = "Forecast_mean"
            else:
                raise VisualizationError(
                    "West-WRF only provides Control Forecast and Ensemble Mean "
                    "AR Scale maps (no Observed)."
                )
            return (
                "https://cw3e.ucsd.edu/images/wwrf/images/ensemble/ARScale/"
                f"ARScale_PlumeMap_{suffix}.png"
            )

        model_info = MODELS[self.model]
        model = model_info["code"]
        interval = model_info["cycle_interval"]
        location = LOCATION_CODES[self.location]

        precip = PRECIP_TOKENS[self.plot_type] if self.show_precipitation else ""
        product = f"arscale_{precip}map_{PLOT_CODES[self.plot_type]}"

        if self.date == "latest":
            return self._resolve_latest_url(model, interval, product, location)

        # Validate the requested run cycle for the selected model.
        if self.date.hour % interval != 0:
            valid = ", ".join(f"{h:02d}Z" for h in range(0, 24, interval))
            raise VisualizationError(
                f"{self.model} model runs are only available at {valid}."
            )

        date_str = self.date.strftime("%Y%m%d%H")
        return self._build_url(product, model, location, date_str)

    def _build_url(self, product, model, location, date_str):
        return (
            f"{BASE_URL}/{product}/v1/{model}/{location}/{date_str}/1/"
            f"{product}__v1__{model}__{location}__{date_str}__1__F168.png"
        )

    def _resolve_latest_url(self, model, interval, product, location):
        """Probe model run cycles backwards to find the newest available run."""
        # Round the current time down to the nearest valid run cycle.
        now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
        cycle = now.replace(hour=(now.hour // interval) * interval)

        # Look back up to ~10 days worth of run cycles.
        for _ in range((10 * 24) // interval):
            date_str = cycle.strftime("%Y%m%d%H")
            url = self._build_url(product, model, location, date_str)
            try:
                if requests.head(url, timeout=10).status_code == 200:
                    return url
            except requests.RequestException:
                pass
            cycle -= timedelta(hours=interval)

        raise VisualizationError(
            f"No AR Scale map image found for {self.model} "
            f"({self.plot_type}, {location}) in the last 10 days."
        )
