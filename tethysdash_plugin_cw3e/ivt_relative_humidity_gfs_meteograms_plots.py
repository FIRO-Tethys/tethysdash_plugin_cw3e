from datetime import datetime, timedelta, timezone
import requests
from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin
from tethysapp.tethysdash.exceptions import VisualizationError

BASE_URL = "https://cw3e.ucsd.edu/images"

# model display label -> v1 model path code and run-cycle interval (hours).
# GFS runs every 6 hours (00/06/12/18Z); ECMWF runs only at 00Z and 12Z.
MODELS = {
    "GFS": {"code": "GFS_25", "cycle_interval": 6},
    "ECMWF": {"code": "ECMWF_HRes", "cycle_interval": 12},
}

# plot_type value -> (v1 product, forecast hour token). 3-day plots run to F072,
# 7-day plots to F168.
PLOT_TYPE_PRODUCTS = {
    "3DayWVFlux": ("watervaporflux_3day_meteogram", "F072"),
    "3DayRH": ("rh_3day_meteogram", "F072"),
    "7DayWVFlux": ("watervaporflux_7day_meteogram", "F168"),
    "7DayRH": ("rh_7day_meteogram", "F168"),
}


class IVTAndRelativeHumidityPlots(TethysDashPlugin):
    name = "cw3e_ivt_and_relative_humidity_plots"
    tags = [
        "cw3e",
        "ar",
        "relative",
        "humidity",
        "ivt",
    ]
    description = "Meteograms that illustrate the forecasted conditions over a given locations for the 3 or 7-day forecast period from the GFS. The top panel includes water vapor flux (kg m-2s-1) or relative humidity (%) shaded with the 0°C isotherm contour and wind barbs(m/s), gray shading indicates location elevation. The middle plot illustrates the 3-hour precipitation represented by the bars, total 72-hour precipitation, height of the 0oC isotherm, and location elevation. When the freezing level is below the location elevation, line and bars are blue representing the likelihood of snow and when the freezing level is above the location elevation line and bars are green representing the likelihood of rain. The bottom plot illustrates the IWV and IVT, as well as the presence of AR conditions shaded in gray. More information can be found at https://cw3e.ucsd.edu/iwv-and-ivt-forecasts/"
    args = {
        "date": "date",
        "latitude": [{"value": lat, "label": f"{lat} N"} for lat in range(26, 51)],
        "longitude": [{"value": lon, "label": f"{lon} W"} for lon in range(111, 128)],
        "visualization": [
            "Map",
            {
                "value": "Plot",
                "label": "Plot",
                "sub_args": {
                    "model": ["GFS", "ECMWF"],
                    "plot_type": [
                        {"value": "3DayWVFlux", "label": "3-day WV Flux"},
                        {"value": "3DayRH", "label": "3-day Relative Humidity"},
                        {"value": "7DayWVFlux", "label": "7-day WV Flux"},
                        {"value": "7DayRH", "label": "7-day Relative Humidity"},
                    ],
                },
            },
        ],
    }
    group = "CW3E"
    label = "IVT and Relative Humidity Plots"
    type = "image"
    attribution = "CW3E"

    def __init__(self, latitude, longitude, visualization, metadata=None, **kwargs):
        # store important kwargs
        self.latitude = latitude
        self.longitude = longitude
        self.visualization = visualization
        self.model = kwargs.get("visualization.model")
        self.plot_type = kwargs.get("visualization.plot_type")

        if int(longitude) < 0:
            self.longitude = int(longitude) * -1
        # Pass kwargs through so the base class parses/sets the "date" arg.
        super().__init__(metadata=metadata, **kwargs)

    def run(self):
        # The location map has no v1 product; keep it on the legacy URL.
        if self.visualization == "Map":
            return (
                f"{BASE_URL}/gfs/Meteograms/maps/"
                f"Meteo_maps{self.latitude}_{self.longitude}.png"
            )

        model_info = MODELS[self.model]
        model = model_info["code"]
        interval = model_info["cycle_interval"]
        product, forecast_hour = PLOT_TYPE_PRODUCTS[self.plot_type]
        location = f"{self.latitude}N_{self.longitude}W"

        if self.date == "latest":
            return self._resolve_latest_url(
                product, model, interval, location, forecast_hour
            )

        # Validate the requested run cycle for the selected model.
        if self.date.hour % interval != 0:
            valid = ", ".join(f"{h:02d}Z" for h in range(0, 24, interval))
            raise VisualizationError(
                f"{self.model} model runs are only available at {valid}."
            )

        date_str = self.date.strftime("%Y%m%d%H")
        return self._build_url(product, model, location, date_str, forecast_hour)

    def _build_url(self, product, model, location, date_str, forecast_hour):
        return (
            f"{BASE_URL}/{product}/v1/{model}/{location}/{date_str}/1/"
            f"{product}__v1__{model}__{location}__{date_str}__1__{forecast_hour}.png"
        )

    def _resolve_latest_url(self, product, model, interval, location, forecast_hour):
        """Probe model run cycles backwards to find the newest available run."""
        # Round the current time down to the nearest valid run cycle.
        now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
        cycle = now.replace(hour=(now.hour // interval) * interval)

        # Look back up to ~10 days worth of run cycles.
        for _ in range((10 * 24) // interval):
            date_str = cycle.strftime("%Y%m%d%H")
            url = self._build_url(product, model, location, date_str, forecast_hour)
            try:
                if requests.head(url, timeout=(3, 5)).status_code == 200:
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
            f"No meteogram image found for {self.model} "
            f"({self.plot_type}, {location}) in the last 10 days."
        )
