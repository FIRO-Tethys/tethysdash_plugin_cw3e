"""AR Scale plume diagram for a radiosonde launch site.

Shows the same CW3E plume diagrams as ar_scale_plume_diagrams.py, at the
point the site registry assigns each launch site, so a dashboard's site
selector can drive it without choosing a transect and location by hand.
"""

from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin

from .ar_scale_plume_diagrams import ARScalePlumeDiagrams
from .radiosonde_sites import SITE_ARG, get_launch_site

PLUME_ARGS = ARScalePlumeDiagrams.args


class LaunchSiteARScalePlume(TethysDashPlugin):
    name = "cw3e_launch_site_ar_scale_plume"
    tags = ["cw3e", "ar", "scale", "plume", "radiosonde", "launch"]
    description = (
        "CW3E AR Scale plume diagram at the forecast point nearest a "
        "radiosonde launch site: the integrated water vapor transport (IVT) "
        "and AR Scale forecast over the next 7 days. More information can be "
        "found at https://cw3e.ucsd.edu/arscale/"
    )
    args = {
        "site": SITE_ARG,
        "date": PLUME_ARGS["date"],
        "plot_type": PLUME_ARGS["plot_type"],
        "model": PLUME_ARGS["model"],
        "AR_scale_calculated_by": PLUME_ARGS["AR_scale_calculated_by"],
    }
    group = "CW3E"
    label = "Launch Site AR Scale Plume"
    type = "image"
    attribution = "CW3E"

    def run(self):
        site = get_launch_site(self.site)
        # The plume plugin parses its date again: pass presets ("latest")
        # as they are and parsed dates as ISO text.
        date = self.date if isinstance(self.date, str) else self.date.isoformat()
        plume = ARScalePlumeDiagrams(
            plot_type=self.plot_type,
            transect_location=site.ar_transect,
            model=self.model,
            AR_scale_calculated_by=self.AR_scale_calculated_by,
            date=date,
            **{"transect_location.location": site.ar_location},
        )
        return plume.run()
