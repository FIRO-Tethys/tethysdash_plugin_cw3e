from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import requests
import numpy as np
import pytz
from datetime import datetime


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


class PhotoExplorerDataTimeSeries(TethysDashPlugin):
    name = "usgs_photo_explorer_time_series"
    args = {
        "station": get_stations(),
        "start_date": "date",
        "end_date": "date",
    }
    group = "USGS"
    label = "Station Data Time Series"
    type = "plotly"
    tags = [
        "usgs",
        "time series",
    ]
    attribution = "USGS Photo Explorer"
    description = "Plots time series data from the photo explorer API"

    def run(self):
        # First, get the station info to retrieve the timezone
        station_url = f"https://drekttvuk1.execute-api.us-west-2.amazonaws.com/api/public/stations/{self.station}/"
        station_req = requests.get(station_url)
        if station_req.status_code != 200:
            raise Exception(
                f"Could not retrieve station information for station {self.station}."
            )

        station_info = station_req.json()
        station_timezone = station_info.get("timezone", "UTC")
        station_name = station_info.get("name", self.station)

        # Get timezone object for the station
        try:
            tz = pytz.timezone(station_timezone)
        except pytz.UnknownTimeZoneError:
            # Fallback to UTC if timezone is unknown
            tz = pytz.UTC

        # Get available variables from station summary
        available_variables = []
        if "summary" in station_info and "values" in station_info["summary"]:
            available_variables = [
                var["variable_id"]
                for var in station_info["summary"]["values"]["variables"]
            ]

        # Define variable configurations: variable_id, name, color, yaxis
        variable_configs = {
            "FLOW_CFS": {"name": "Flow (CFS)", "color": "blue", "yaxis": "y"},
            "STAGE_FT": {"name": "Stage (FT)", "color": "orange", "yaxis": "y2"},
            "WTEMP_C": {
                "name": "Water Temp (°C)",
                "color": "green",
                "yaxis": "y3",
            },
        }

        # Default colors for unknown variables
        default_colors = ["red", "purple", "brown", "pink", "gray", "olive", "cyan"]
        color_index = 0

        # Fetch data for available variables
        variable_data = {}
        for var_id in available_variables:
            data_url = f"https://drekttvuk1.execute-api.us-west-2.amazonaws.com/api/public/stations/{self.station}/values?variable={var_id}&start={self.start_date}&end={self.end_date}"
            data_req = requests.get(data_url)
            if data_req.status_code == 200:
                df = pd.DataFrame(data_req.json())
                if not df.empty:
                    # Convert timestamps from UTC to local timezone
                    df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.tz_convert(tz)
                    variable_data[var_id] = df

                    # Add default configuration for unknown variables
                    if var_id not in variable_configs:
                        # Create a readable name from variable_id
                        name = var_id.replace("_", " ").title()
                        # Assign a default color
                        color = default_colors[color_index % len(default_colors)]
                        color_index += 1
                        # Assign each variable its own y-axis
                        # Count existing axes to determine next available axis number
                        existing_axes = len(
                            [
                                k
                                for k in variable_configs.keys()
                                if k in variable_data or k == var_id
                            ]
                        )
                        yaxis_name = "y" if existing_axes == 1 else f"y{existing_axes}"

                        variable_configs[var_id] = {
                            "name": name,
                            "color": color,
                            "yaxis": yaxis_name,
                        }

        # Create figure with multiple y-axes
        fig = go.Figure()

        # Add traces for each available variable
        for i, (var_id, df) in enumerate(variable_data.items()):
            config = variable_configs[var_id]

            fig.add_trace(
                go.Scatter(
                    x=df["timestamp"],
                    y=df["value"],
                    mode="lines",
                    name=config["name"],
                    line=dict(color=config["color"], width=2),
                    yaxis=f"y{i+1}" if i > 0 else "y",
                )
            )

        # Update layout with multiple y-axes
        layout_updates = {
            "title": {
                "text": f"Station {station_name}",
                "x": 0.5,  # Center the title horizontally
                "xanchor": "center",  # Anchor at center
            },
            "plot_bgcolor": "white",
            "paper_bgcolor": "white",
            "showlegend": True,
            "height": 500,  # Increased height to accommodate legend
            "hovermode": "x unified",
            # Center the chart and position legend to avoid covering axes
            "legend": {
                "orientation": "h",  # Horizontal legend
                "yanchor": "top",
                "y": -0.2,  # Position below the chart
                "xanchor": "center",
                "x": 0.5,  # Center horizontally
            },
            # Add margins to center the chart and leave space for legend
            "margin": {
                "l": 80,  # Left margin for y-axis labels
                "r": 80,  # Right margin for y-axis labels
                "t": 50,  # Top margin for title
                "b": 100,  # Bottom margin for legend
            },
        }

        # Configure x-axis - autoshift will handle spacing automatically
        layout_updates["xaxis"] = {
            "showgrid": True,
            "gridwidth": 1,
            "gridcolor": "lightgray",
            "title": "Time",
            "linecolor": "black",
            "linewidth": 1,
            "mirror": True,
            "ticks": "outside",
        }

        # Configure individual y-axes for each variable using autoshift
        axis_positions = ["left", "right"]  # Alternate sides
        for i, (var_id, _) in enumerate(variable_data.items()):
            config = variable_configs[var_id]

            # Determine side (left/right alternating)
            side = axis_positions[i % 2]

            # Configure y-axis
            yaxis_name = "yaxis" if i == 0 else f"yaxis{i+1}"

            if i == 0:
                # Primary y-axis (first one)
                layout_updates[yaxis_name] = {
                    "title": {
                        "text": config["name"],
                        "font": {"color": config["color"]},
                    },
                    "tickcolor": config["color"],
                    "tickfont": {"color": config["color"]},
                    "showgrid": True,
                    "gridwidth": 1,
                    "gridcolor": "lightgray",
                    "linecolor": config["color"],
                    "linewidth": 2,
                    "mirror": True,
                    "ticks": "outside",
                }
            elif i == 1:
                # Second axis - standard right side without autoshift
                layout_updates[yaxis_name] = {
                    "title": {
                        "text": config["name"],
                        "font": {"color": config["color"]},
                    },
                    "tickcolor": config["color"],
                    "tickfont": {"color": config["color"]},
                    "overlaying": "y",
                    "side": "right",
                    "showgrid": False,
                    "linecolor": config["color"],
                    "linewidth": 2,
                    "mirror": True,
                    "ticks": "outside",
                }
            else:
                # Additional axes - use autoshift for automatic positioning
                layout_updates[yaxis_name] = {
                    "title": {
                        "text": config["name"],
                        "font": {"color": config["color"]},
                    },
                    "tickcolor": config["color"],
                    "tickfont": {"color": config["color"]},
                    "anchor": "free",
                    "overlaying": "y",
                    "autoshift": True,
                    "showgrid": False,
                    "linecolor": config["color"],
                    "linewidth": 2,
                    "mirror": True,
                    "ticks": "outside",
                }

        fig.update_layout(layout_updates)

        return json.loads(fig.to_json())
