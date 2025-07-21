from intake.source import base


class QPE(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "cw3e_qpe"
    visualization_tags = ["cw3e", "noaa", "qpe", "precipitation"]
    visualization_description = "Gridded precipitation data are the National Stage IV Quantitative Precipitation Estimate (QPE) Product, provided by the NOAA/NCEP/EMC and PRISM daily precipitation estimate from PRISM Climate Group, Oregon State University. More information can be found at https://cw3e.ucsd.edu/precipitation-observations/#WYTD"
    visualization_args = {
        "time_range": [
            {"label": "Past 1 Hour", "value": "HourlyPrecip"},
            {"label": "Past 6 Hours", "value": "SixHrPrecip"},
            {"label": "Past 24 Hours", "value": "Daily_Precip"},
            {"label": "Past Week", "value": "Weekly_Precip"},
            {"label": "Water Year", "value": "water_year"},
            {
                "label": "Water Year Comparison",
                "value": "water_year_comparison",
                "sub_args": {
                    "plot_type": [
                        {"value": "PrecipAnomaly", "label": "Anomaly"},
                        {
                            "value": "DepartureFromNormal",
                            "label": "Departure from Normal",
                        },
                        {"value": "NormalPrecip", "label": "Normal"},
                    ],
                },
            },
        ],
    }
    visualization_group = "CW3E"
    visualization_label = "National Stage IV QPE"
    visualization_type = "image"

    def __init__(self, time_range, metadata=None, **kwargs):
        # store important kwargs
        self.time_range = time_range
        self.comparison = kwargs.get("time_range.plot_type")
        super().__init__(metadata=metadata)

    def read(self):
        if self.time_range == "HourlyPrecip":
            return "https://cw3e.ucsd.edu/images/precip/Hourly_Precip/HourlyPrecip_Latest.png"

        if self.time_range == "water_year":
            return f"https://cw3e.ucsd.edu/images/precip/PRISM/Daily/WYTD_Precip.png"

        if self.time_range == "water_year_comparison":
            return f"https://cw3e.ucsd.edu/images/precip/PRISM/Daily/WYTD_{self.comparison}.png"

        return f"https://cw3e.ucsd.edu/images/precip/{self.time_range}/{self.time_range}_Latest.png"
