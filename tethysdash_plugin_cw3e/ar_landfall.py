from datetime import datetime, timedelta, timezone
import requests
from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin
from tethysapp.tethysdash.exceptions import VisualizationError
from .constants import (
    ARLandfallBaseUrl,
    ARLandfallModelLocationOptions,
    ARLandfallModelTypeOptions,
    ARLandfallModelOptions,
)

# data_source display label -> v1 landfall-tool model path code.
NEW_SCHEME_MODELS = {
    "GFS Ensemble": "GEFS_50",
    "ECMWF EPS": "ECMWF_ENS",
    "ECMWF minus GFS": "ECMWF_ENS-GEFS_50",
}

# model_type display label -> (v1 product path component, forecast hour token).
# Vectors products run to F168; all others run to F384.
PRODUCT_CODES = {
    "Control IVT magnitude": ("ivtcontrol", "F384"),
    "Ensemble mean magnitude": ("ivtmean", "F384"),
    "Probability of IVT >150 kg/m/s": ("ivt150_probability", "F384"),
    "Probability of IVT >250 kg/m/s": ("ivt250_probability", "F384"),
    "Probability of IVT >500 kg/m/s": ("ivt500_probability", "F384"),
    "Probability of IVT >750 kg/m/s": ("ivt750_probability", "F384"),
    "IVT >150 kg/m/s with Vectors": ("ivt150_vectors", "F168"),
    "IVT >250 kg/m/s with Vectors": ("ivt250_vectors", "F168"),
    "IVT >500 kg/m/s with Vectors": ("ivt500_vectors", "F168"),
    "IVT >750 kg/m/s with Vectors": ("ivt750_vectors", "F168"),
}

# "with Vectors" model types are published for GFS Ensemble and ECMWF EPS, but
# not for the ECMWF-minus-GFS difference field.
VECTOR_MODEL_TYPES = {
    "IVT >150 kg/m/s with Vectors",
    "IVT >250 kg/m/s with Vectors",
    "IVT >500 kg/m/s with Vectors",
    "IVT >750 kg/m/s with Vectors",
}
VECTOR_CAPABLE_SOURCES = {"GFS Ensemble", "ECMWF EPS"}

# model_location display label -> v1 location path component.
LOCATION_CODES = {
    "Coastal": "coast",
    "Foothills": "foothills",
    "Inland": "inland",
    "Interior West": "intwest",
}

# West-WRF is not on the v1 scheme (and is not run in real-time); it uses the
# legacy "_current.png" landfall-tool URL. model_type / model_location -> suffix.
WEST_WRF_TYPE_SUFFIXES = {
    "Control IVT magnitude": "_control",
    "Ensemble mean magnitude": "_ensemble_mean",
    "Probability of IVT >150 kg/m/s": "_150",
    "Probability of IVT >250 kg/m/s": "_250",
    "Probability of IVT >500 kg/m/s": "_500",
    "Probability of IVT >750 kg/m/s": "_750",
    "IVT >150 kg/m/s with Vectors": "_Vectors_150",
    "IVT >250 kg/m/s with Vectors": "_Vectors_250",
    "IVT >500 kg/m/s with Vectors": "_Vectors_500",
    "IVT >750 kg/m/s with Vectors": "_Vectors_750",
}
WEST_WRF_LOCATION_SUFFIXES = {
    "Coastal": "_coast",
    "Foothills": "_foothills",
    "Inland": "_inland",
    "Interior West": "_intwest",
}


class ARLandfall(TethysDashPlugin):
    name = "cw3e_ar_landfall"
    args = {
        "date": "date",
        "data_source": ARLandfallModelOptions,
        "model_type": ARLandfallModelTypeOptions,
        "model_location": ARLandfallModelLocationOptions,
    }
    group = "CW3E"
    label = "AR Landfall Tool"
    type = "image"
    tags = [
        "cw3e",
        "ar",
        "landfall",
        "gfs",
        "gefs",
        "ecmwf",
        "wrf",
        "probability",
        "coastal",
    ]
    description = "Displays the likelihood and timing of AR conditions at each point on the map in a line. Conditions for multiple models, AR types, and locations can be chosen. More information about individual AR products can be found at https://cw3e.ucsd.edu/iwv-and-ivt-forecasts/"

    def run(self):
        """Return the AR landfall image URL"""
        # West-WRF has no v1 product (not run in real-time); use the legacy URL.
        if self.data_source == "West-WRF Ensemble":
            return (
                f"{ARLandfallBaseUrl}wwrf/images/ensemble/LFT/US-west/"
                f"W-WRF_LandfallTool{WEST_WRF_TYPE_SUFFIXES[self.model_type]}"
                f"{WEST_WRF_LOCATION_SUFFIXES[self.model_location]}_current.png"
            )

        # The only unavailable combination is the ECMWF-minus-GFS difference
        # field with vectors, which is not published in any scheme.
        if (
            self.data_source == "ECMWF minus GFS"
            and self.model_type in VECTOR_MODEL_TYPES
        ):
            raise VisualizationError(
                "Vectors products are not available for the ECMWF minus GFS "
                "difference field."
            )

        model = NEW_SCHEME_MODELS[self.data_source]
        product, forecast_hour = PRODUCT_CODES[self.model_type]
        location = LOCATION_CODES[self.model_location]

        if self.date == "latest":
            return self._resolve_latest_url(model, product, location, forecast_hour)

        date_str = self.date.strftime("%Y%m%d%H")
        return self._build_url(model, product, location, date_str, forecast_hour)

    def _build_url(self, model, product, location, date_str, forecast_hour):
        return (
            f"{ARLandfallBaseUrl}landfalltool_{product}/v1/{model}/{location}/"
            f"{date_str}/1/landfalltool_{product}__v1__{model}__{location}__"
            f"{date_str}__1__{forecast_hour}.png"
        )

    def _resolve_latest_url(self, model, product, location, forecast_hour):
        """Probe synoptic cycles backwards to find the newest available image."""
        # GEFS runs every 6 hours (00/06/12/18Z); ECMWF and the difference at
        # 00/12Z. Round the current time down to the nearest valid run cycle.
        interval = 6 if self.data_source == "GFS Ensemble" else 12
        now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
        cycle = now.replace(hour=(now.hour // interval) * interval)

        # Look back up to ~10 days worth of run cycles.
        for _ in range((10 * 24) // interval):
            date_str = cycle.strftime("%Y%m%d%H")
            url = self._build_url(model, product, location, date_str, forecast_hour)
            try:
                if requests.head(url, timeout=(3, 5)).status_code == 200:
                    return url
            except requests.RequestException:
                # Site unreachable (e.g. a blocked IP). CW3E products lag their
                # synoptic cycle by several hours, so fall back to the newest
                # cycle ~12h old (which has realistically finished) instead of
                # the current one, which usually is not published yet. Rounded
                # to the model's cycle step.
                fallback = now - timedelta(hours=12)
                fallback_str = fallback.replace(
                    hour=(fallback.hour // interval) * interval,
                ).strftime("%Y%m%d%H")
                return url.replace(date_str, fallback_str)
            cycle -= timedelta(hours=interval)

        raise VisualizationError(
            f"No AR Landfall Tool image found for {self.data_source} "
            f"({self.model_type}, {self.model_location}) in the last 10 days."
        )
