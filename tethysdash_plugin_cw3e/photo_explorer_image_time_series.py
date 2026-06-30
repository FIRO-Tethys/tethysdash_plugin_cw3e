from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin
import pandas as pd
import plotly.express as px
import json
import requests
from datetime import datetime, timedelta
import pytz
from tethysapp.tethysdash.exceptions import VisualizationError


def get_stations():
    url = "https://drekttvuk1.execute-api.us-west-2.amazonaws.com/api/public/stations"
    response = requests.get(url)
    if response.status_code == 200:
        station_metadata = response.json()
        return [
            {"value": station["id"], "label": station["name"]}
            for station in station_metadata
        ]
    else:
        return []


class PhotoExplorerImageTimeSeries(TethysDashPlugin):
    name = "usgs_photo_explorer_image_time_series"
    args = {
        "station": get_stations(),
        "date": "date-hour",
    }
    group = "USGS"
    label = "Station Image Time Series"
    type = "image"
    tags = [
        "usgs",
        "time series",
    ]
    description = (
        "Plots image time series data from the photo explorer API"
    )
    attribution = "USGS Photo Explorer"
    loading_icon = False

    def run(self):
        # First, get the station info to retrieve the timezone
        station_url = f"https://drekttvuk1.execute-api.us-west-2.amazonaws.com/api/public/stations/{self.station}/"
        station_req = requests.get(station_url)
        if station_req.status_code != 200:
            raise VisualizationError(
                f"Could not retrieve station information for station {self.station}."
            )

        station_info = station_req.json()
        station_timezone = station_info.get("timezone", "UTC")

        try:
            parsed_date = datetime.strptime(self.date, "%m/%d/%Y %H:%M")
        except ValueError:
            parsed_date = datetime.strptime(self.date, "%Y-%m-%d %H:%M")

        # The API expects dates in the station's local timezone
        formatted_date = datetime.strftime(
            parsed_date - timedelta(hours=12), "%Y-%m-%dT%H:%M"
        )
        end_formatted_date = datetime.strftime(
            parsed_date + timedelta(days=12), "%Y-%m-%dT%H:%M"
        )
        images_url = f"https://drekttvuk1.execute-api.us-west-2.amazonaws.com/api/public/stations/{self.station}/images?start={formatted_date}&end={end_formatted_date}"

        station_data_images_req = requests.get(images_url)
        station_data_images = station_data_images_req.json()

        if not station_data_images:
            raise VisualizationError(f"No photo available for {self.date}.")

        # Find the photo closest to the desired hour
        closest_photo = None
        min_hour_diff = float("inf")
        target_hour = parsed_date.hour  # Get hour from parsed date (in local timezone)

        # Get timezone object for the station
        try:
            tz = pytz.timezone(station_timezone)
        except pytz.UnknownTimeZoneError:
            # Fallback to UTC if timezone is unknown
            tz = pytz.UTC

        for photo in station_data_images:
            # Parse UTC timestamp
            photo_timestamp_utc = datetime.fromisoformat(
                photo["timestamp"].replace("Z", "+00:00")
            )
            # Convert to station's local timezone
            photo_timestamp_local = photo_timestamp_utc.astimezone(tz)
            photo_hour = photo_timestamp_local.hour
            hour_diff = abs(photo_hour - target_hour)

            if hour_diff < min_hour_diff:
                min_hour_diff = hour_diff
                closest_photo = photo

        if closest_photo is None:
            raise VisualizationError(
                f"No suitable photo found for hour {target_hour} on {self.date}."
            )

        return closest_photo["thumb_url"]
