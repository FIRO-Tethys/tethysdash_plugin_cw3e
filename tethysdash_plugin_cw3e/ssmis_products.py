from intake.source import base


class SSMISProducts(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "ssmis_products"
    visualization_tags = [
        "cw3e",
        "noaa",
        "water vapor",
        "rain rate",
        "cloud liquid water",
    ]
    visualization_description = "Displays the latest SSMIS water data products. More information can be found at https://cw3e.ucsd.edu/satellite/#ARD"
    visualization_args = {
        "domain": [
            {"label": "Pacific", "value": "6hr"},
            {"label": "US West Coast", "value": "hi"},
        ],
        "data_type": [
            {"label": "Water Vapor", "value": "recent"},
            {"label": "Cloud Liquid Water", "value": "recent_clw"},
            {"label": "Rain Rate", "value": "recent_rn2"},
        ],
    }
    visualization_group = "CW3E"
    visualization_label = "SSMIS Products"
    visualization_type = "image"

    def __init__(self, domain, data_type, metadata=None):
        # store important kwargs
        self.domain = domain
        self.data_type = data_type
        super().__init__(metadata=metadata)

    def read(self):

        return f"http://www.esrl.noaa.gov/psd/psd2/coastal/satres/data/images/wx_cl/P3/{self.domain}/{self.data_type}.png"
