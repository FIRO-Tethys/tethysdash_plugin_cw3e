from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin


class SSMISProducts(TethysDashPlugin):
    name = "noaa_ssmis_products"
    tags = [
        "cw3e",
        "noaa",
        "water vapor",
        "rain rate",
        "cloud liquid water",
    ]
    description = "Displays the latest SSMIS water data products. More information can be found at https://cw3e.ucsd.edu/satellite/#ARD"
    args = {
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
    group = "NOAA"
    label = "SSMIS Products"
    type = "image"
    attribution = "NOAA"

    def run(self):

        return f"http://www.esrl.noaa.gov/psd/psd2/coastal/satres/data/images/wx_cl/P3/{self.domain}/{self.data_type}.png"
