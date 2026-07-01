from datetime import datetime, timedelta, timezone
import requests
from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin
from tethysapp.tethysdash.exceptions import VisualizationError

BASE_URL = "https://cw3e.ucsd.edu/images"

# model display label -> v1 model path code, run-cycle interval (hours), and
# whether it is the ECMWF-minus-GFS difference product (different product name).
# GFS runs every 6 hours (00/06/12/18Z); ECMWF and the difference run at 00/12Z.
MODELS = {
    "GFS": {"code": "GFS_25", "cycle_interval": 6, "difference": False},
    "ECMWF": {"code": "ECMWF_HRes", "cycle_interval": 12, "difference": False},
    "ECMWF-GFS": {
        "code": "ECMWF_HRes-GFS_25",
        "cycle_interval": 12,
        "difference": True,
    },
}

# Both models produce forecasts every 3 hours.
FORECAST_INTERVAL_HOURS = 3


class IVTAndIWVAnalysesAndForecasts(TethysDashPlugin):
    name = "cw3e_ivt_and_iwv_analyses_and_forecasts"
    tags = [
        "cw3e",
        "ar",
        "ivt",
        "gfs",
        "ecmwf",
        "iwv",
    ]
    description = "Vertically Integrated Water Vapor Transport (IVT) with magnitude shaded in units of kg m-1 s-1, direction indicated by vectors and mean sea level pressure contoured in hPa. Integrated water vapor (IWV) with magnitude shaded in units of mm, 850-hPa wind vectors, and mean sea level pressure contoured in hPa. More information can be found at https://cw3e.ucsd.edu/ivt_iwv_npacific/"
    args = {
        "date": "date",
        "model": ["GFS", "ECMWF", "ECMWF-GFS"],
        "product": [{"value": "ivt", "label": "IVT"}, {"value": "iwv", "label": "IWV"}],
        "forecast_hour": "number",
        "region": [
            {"value": "NPac", "label": "North Pacific"},
            {"value": "NEPac", "label": "Northeast Pacific"},
            {"value": "USWC", "label": "U.S. West Coast"},
            {"value": "IntWest", "label": "Interior West"},
            {"value": "NAmerica", "label": "North America"},
            {"value": "NAtlantic", "label": "North Atlantic"},
        ],
    }
    group = "CW3E"
    label = "IVT and IWV Analyses and Forecasts"
    type = "image"
    loading_icon = False
    attribution = "CW3E"

    def run(self):
        if self.model != "GFS" and self.region == "NAtlantic":
            raise VisualizationError(
                "ECMWF model is not available for the North Atlantic region."
            )

        if self.model == "ECMWF-GFS" and self.region == "NAmerica":
            raise VisualizationError(
                "ECMWF-GFS model is not available for the North America region."
            )

        model_info = MODELS[self.model]
        model = model_info["code"]
        interval = model_info["cycle_interval"]
        suffix = "_difference_map" if model_info["difference"] else "_map"
        product = f"{self.product}{suffix}"
        region = self.region
        forecast_hour = self._format_forecast_hour()

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
            f"No {self.product.upper()} image found for {self.model} "
            f"({region}, {forecast_hour}) in the last 10 days."
        )
