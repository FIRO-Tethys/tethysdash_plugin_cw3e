from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin


class WaterVaporFlux(TethysDashPlugin):
    name = "noaa_water_vapor_flux"
    tags = ["cw3e", "noaa", "water", "vapor", "flux"]
    description = "Shows wind at various levels colored by speed, freezing layer (black dots/dashed line), integrated water vapor (cyan line), upslope wind speed (purple or brown bars), upslope integrated water vapor flux (blue line), and hourly precipitation (green or red bars) with time moving from right to left. More information can be found at https://cw3e.ucsd.edu/real-time-observations/"
    args = {
        "location": [
            {"label": "Astoria, OR", "value": "ast"},
            {"label": "Bodega Bay, CA", "value": "bby"},
            {"label": "Forks, WA", "value": "fks"},
            {"label": "McKinleyville, CA", "value": "acv"},
            {"label": "North Bend, OR", "value": "oth"},
            {"label": "Oroville, CA", "value": "ove"},
            {"label": "Point Sur, CA", "value": "pts"},
            {"label": "Santa Barbara, CA", "value": "sba"},
            {"label": "Twitchell Island, CA", "value": "tci"},
        ],
        "display_type": [
            {"label": "Map", "value": "Map"},
            {
                "label": "Plot",
                "value": "Plot",
                "sub_args": {
                    "data_source": [
                        {"label": "Observations", "value": "iwvflux"},
                        {"label": "HRRR Model", "value": "iwvflux_hrrr"},
                        {"label": "RAP Model", "value": "iwvflux_rap"},
                    ],
                },
            },
        ],
    }
    group = "NOAA"
    label = "Water Vapor Flux Analyses and Forecasts"
    type = "image"
    attribution = "NOAA"

    def __init__(self, location, display_type, metadata=None, **kwargs):
        # store important kwargs
        self.location = location
        self.display_type = display_type
        self.data_source = kwargs.get("display_type.data_source")
        super().__init__(metadata=metadata)

    def run(self):
        if self.display_type == "Map":
            return f"https://cw3e.ucsd.edu/images/aro/maps/WVFlux_{self.location}.png"

        return f"https://cw3e.ucsd.edu/images/aro/images/{self.location}_{self.data_source}.gif"
