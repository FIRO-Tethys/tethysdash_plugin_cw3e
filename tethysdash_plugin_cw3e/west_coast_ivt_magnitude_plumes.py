from datetime import datetime, timedelta, timezone
import requests
from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin
from tethysapp.tethysdash.exceptions import VisualizationError

BASE_URL = "https://cw3e.ucsd.edu/images"

# Plot models served by the new v1 scheme -> model path code and run-cycle
# interval (hours). GEFS runs every 6 hours; ECMWF and the combined product at
# 00Z/12Z. West-WRF models have no v1 product and use the legacy URL below.
NEW_SCHEME_MODELS = {
    "GEFS": {"code": "GEFS_50", "cycle_interval": 6},
    "ECMWF": {"code": "ECMWF_ENS", "cycle_interval": 12},
    "GEFS_ECMWF": {"code": "GEFS_50_ECMWF_ENS", "cycle_interval": 12},
}

# West-WRF plume models -> legacy URL path prefix (no v1 product yet).
LEGACY_MODEL_BASES = {
    "WWRF": "wwrf/ensemble/IVTPlumes/West-WRF",
    "WWRF_GEFS_ECMWF": "wwrf/ensemble/IVTPlumes/GEFS_ECMWF_West-WRF",
}

coastal_locations = [
    {"value": "60.0_220.0", "label": "60.0N 140.0W"},
    {"value": "59.5_220.5", "label": "59.5N 139.5W"},
    {"value": "59.0_221.5", "label": "59.0N 138.5W"},
    {"value": "58.5_222.5", "label": "58.5N 137.5W"},
    {"value": "58.0_223.5", "label": "58.0N 136.5W"},
    {"value": "57.5_224.0", "label": "57.5N 136.0W"},
    {"value": "57.0_224.5", "label": "57.0N 135.5W"},
    {"value": "56.5_225.0", "label": "56.5N 135.0W"},
    {"value": "56.0_225.5", "label": "56.0N 134.5W"},
    {"value": "55.5_226.5", "label": "55.5N 133.5W"},
    {"value": "55.0_227.0", "label": "55.0N 133.0W"},
    {"value": "54.5_229.5", "label": "54.5N 130.5W"},
    {"value": "54.0_230.0", "label": "54.0N 130.0W"},
    {"value": "53.5_230.0", "label": "53.5N 130.0W"},
    {"value": "53.0_230.5", "label": "53.0N 129.5W"},
    {"value": "52.5_231.5", "label": "52.5N 128.5W"},
    {"value": "52.0_232.0", "label": "52.0N 128.0W"},
    {"value": "51.5_232.0", "label": "51.5N 128.0W"},
    {"value": "51.0_232.0", "label": "51.0N 128.0W"},
    {"value": "50.5_232.5", "label": "50.5N 127.5W"},
    {"value": "50.0_233.0", "label": "50.0N 127.0W"},
    {"value": "49.5_234.0", "label": "49.5N 126.0W"},
    {"value": "49.0_235.0", "label": "49.0N 125.0W"},
    {"value": "48.5_235.5", "label": "48.5N 124.5W"},
    {"value": "48.0_235.5", "label": "48.0N 124.5W"},
    {"value": "47.5_235.5", "label": "47.5N 124.5W"},
    {"value": "47.0_236.0", "label": "47.0N 124.0W"},
    {"value": "46.5_236.0", "label": "46.5N 124.0W"},
    {"value": "46.0_236.0", "label": "46.0N 124.0W"},
    {"value": "45.5_236.0", "label": "45.5N 124.0W"},
    {"value": "45.0_236.0", "label": "45.0N 124.0W"},
    {"value": "44.5_236.0", "label": "44.5N 124.0W"},
    {"value": "44.0_236.0", "label": "44.0N 124.0W"},
    {"value": "43.5_236.0", "label": "43.5N 124.0W"},
    {"value": "43.0_235.5", "label": "43.0N 124.5W"},
    {"value": "42.5_235.5", "label": "42.5N 124.5W"},
    {"value": "42.0_236.0", "label": "42.0N 124.0W"},
    {"value": "41.5_236.0", "label": "41.5N 124.0W"},
    {"value": "41.0_236.0", "label": "41.0N 124.0W"},
    {"value": "40.5_236.0", "label": "40.5N 124.0W"},
    {"value": "40.0_236.0", "label": "40.0N 124.0W"},
    {"value": "39.5_236.5", "label": "39.5N 123.5W"},
    {"value": "39.0_236.5", "label": "39.0N 123.5W"},
    {"value": "38.5_237.0", "label": "38.5N 123.0W"},
    {"value": "38.0_237.0", "label": "38.0N 123.0W"},
    {"value": "37.5_237.5", "label": "37.5N 122.5W"},
    {"value": "37.0_237.5", "label": "37.0N 122.5W"},
    {"value": "36.5_238.0", "label": "36.5N 122.0W"},
    {"value": "36.0_238.5", "label": "36.0N 121.5W"},
    {"value": "35.5_239.0", "label": "35.5N 121.0W"},
    {"value": "35.0_239.5", "label": "35.0N 120.5W"},
    {"value": "34.5_240.0", "label": "34.5N 120.0W"},
    {"value": "34.0_241.5", "label": "34.0N 118.5W"},
    {"value": "33.5_242.5", "label": "33.5N 117.5W"},
    {"value": "33.0_242.5", "label": "33.0N 117.5W"},
    {"value": "32.5_243.0", "label": "32.5N 117.0W"},
    {"value": "32.0_243.0", "label": "32.0N 117.0W"},
    {"value": "31.5_243.5", "label": "31.5N 116.5W"},
    {"value": "31.0_243.5", "label": "31.0N 116.5W"},
    {"value": "30.5_244.0", "label": "30.5N 116.0W"},
    {"value": "30.0_244.5", "label": "30.0N 115.5W"},
    {"value": "29.5_244.5", "label": "29.5N 115.5W"},
    {"value": "29.0_245.5", "label": "29.0N 114.5W"},
    {"value": "28.5_246.0", "label": "28.5N 114.0W"},
    {"value": "28.0_245.5", "label": "28.0N 114.5W"},
    {"value": "27.5_245.5", "label": "27.5N 114.5W"},
    {"value": "27.0_246.0", "label": "27.0N 114.0W"},
    {"value": "26.5_247.0", "label": "26.5N 113.0W"},
    {"value": "26.0_248.0", "label": "26.0N 112.0W"},
    {"value": "25.5_248.0", "label": "25.5N 112.0W"},
    {"value": "25.0_248.0", "label": "25.0N 112.0W"},
]

foothill_locations = [
    {"value": "60.0_223.0", "label": "60.0N 137.0W"},
    {"value": "59.5_223.5", "label": "59.5N 136.5W"},
    {"value": "59.0_224.0", "label": "59.0N 136.0W"},
    {"value": "58.5_224.5", "label": "58.5N 135.5W"},
    {"value": "58.0_225.0", "label": "58.0N 135.0W"},
    {"value": "57.5_225.5", "label": "57.5N 134.5W"},
    {"value": "57.0_226.0", "label": "57.0N 134.0W"},
    {"value": "56.5_226.5", "label": "56.5N 133.5W"},
    {"value": "56.0_227.0", "label": "56.0N 133.0W"},
    {"value": "55.5_228.0", "label": "55.5N 132.0W"},
    {"value": "55.0_229.0", "label": "55.0N 131.0W"},
    {"value": "54.5_230.0", "label": "54.5N 130.0W"},
    {"value": "54.0_231.0", "label": "54.0N 129.0W"},
    {"value": "53.5_231.5", "label": "53.5N 128.5W"},
    {"value": "53.0_232.0", "label": "53.0N 128.0W"},
    {"value": "52.5_233.0", "label": "52.5N 127.0W"},
    {"value": "52.0_233.5", "label": "52.0N 126.5W"},
    {"value": "51.5_234.5", "label": "51.5N 125.5W"},
    {"value": "51.0_235.5", "label": "51.0N 124.5W"},
    {"value": "50.5_236.0", "label": "50.5N 124.0W"},
    {"value": "50.0_237.0", "label": "50.0N 123.0W"},
    {"value": "49.5_238.0", "label": "49.5N 122.0W"},
    {"value": "49.0_238.5", "label": "49.0N 121.5W"},
    {"value": "48.5_238.5", "label": "48.5N 121.5W"},
    {"value": "48.0_238.5", "label": "48.0N 121.5W"},
    {"value": "47.5_238.5", "label": "47.5N 121.5W"},
    {"value": "47.0_238.0", "label": "47.0N 122.0W"},
    {"value": "46.5_238.0", "label": "46.5N 122.0W"},
    {"value": "46.0_238.0", "label": "46.0N 122.0W"},
    {"value": "45.5_238.0", "label": "45.5N 122.0W"},
    {"value": "45.0_238.0", "label": "45.0N 122.0W"},
    {"value": "44.5_237.5", "label": "44.5N 122.5W"},
    {"value": "44.0_237.5", "label": "44.0N 122.5W"},
    {"value": "43.5_237.5", "label": "43.5N 122.5W"},
    {"value": "43.0_237.5", "label": "43.0N 122.5W"},
    {"value": "42.5_237.5", "label": "42.5N 122.5W"},
    {"value": "42.0_237.5", "label": "42.0N 122.5W"},
    {"value": "41.5_237.5", "label": "41.5N 122.5W"},
    {"value": "41.0_237.5", "label": "41.0N 122.5W"},
    {"value": "40.5_238.0", "label": "40.5N 122.0W"},
    {"value": "40.0_238.5", "label": "40.0N 121.5W"},
    {"value": "39.5_239.0", "label": "39.5N 121.0W"},
    {"value": "39.0_239.0", "label": "39.0N 121.0W"},
    {"value": "38.5_239.5", "label": "38.5N 120.5W"},
    {"value": "38.0_239.5", "label": "38.0N 120.5W"},
    {"value": "37.5_240.0", "label": "37.5N 120.0W"},
    {"value": "37.0_241.0", "label": "37.0N 119.0W"},
    {"value": "36.5_241.0", "label": "36.5N 119.0W"},
    {"value": "36.0_241.0", "label": "36.0N 119.0W"},
    {"value": "35.5_241.0", "label": "35.5N 119.0W"},
    {"value": "35.0_241.0", "label": "35.0N 119.0W"},
    {"value": "34.5_241.5", "label": "34.5N 118.5W"},
    {"value": "34.0_242.5", "label": "34.0N 117.5W"},
    {"value": "33.5_243.0", "label": "33.5N 117.0W"},
    {"value": "33.0_243.5", "label": "33.0N 116.5W"},
    {"value": "32.5_243.5", "label": "32.5N 116.5W"},
    {"value": "32.0_243.5", "label": "32.0N 116.5W"},
    {"value": "31.5_244.0", "label": "31.5N 116.0W"},
    {"value": "31.0_244.0", "label": "31.0N 116.0W"},
    {"value": "30.5_244.5", "label": "30.5N 115.5W"},
    {"value": "30.0_245.0", "label": "30.0N 115.0W"},
    {"value": "29.5_245.5", "label": "29.5N 114.5W"},
    {"value": "29.0_246.0", "label": "29.0N 114.0W"},
    {"value": "28.5_246.0", "label": "28.5N 114.0W"},
    {"value": "28.0_246.5", "label": "28.0N 113.5W"},
    {"value": "27.5_247.0", "label": "27.5N 113.0W"},
    {"value": "27.0_247.0", "label": "27.0N 113.0W"},
    {"value": "26.5_247.5", "label": "26.5N 112.5W"},
    {"value": "26.0_248.5", "label": "26.0N 111.5W"},
    {"value": "25.5_248.5", "label": "25.5N 111.5W"},
    {"value": "25.0_248.5", "label": "25.0N 111.5W"},
]

inland_locations = [
    {"value": "60.0_224.0", "label": "60.0N 136.0W"},
    {"value": "59.5_224.5", "label": "59.5N 135.5W"},
    {"value": "59.0_225.0", "label": "59.0N 135.0W"},
    {"value": "58.5_225.5", "label": "58.5N 134.5W"},
    {"value": "58.0_226.0", "label": "58.0N 134.0W"},
    {"value": "57.5_226.5", "label": "57.5N 133.5W"},
    {"value": "57.0_227.0", "label": "57.0N 133.0W"},
    {"value": "56.5_227.5", "label": "56.5N 132.5W"},
    {"value": "56.0_228.5", "label": "56.0N 131.5W"},
    {"value": "55.5_229.0", "label": "55.5N 131.0W"},
    {"value": "55.0_229.5", "label": "55.0N 130.5W"},
    {"value": "54.5_231.0", "label": "54.5N 129.0W"},
    {"value": "54.0_232.0", "label": "54.0N 128.0W"},
    {"value": "53.5_233.0", "label": "53.5N 127.0W"},
    {"value": "53.0_234.0", "label": "53.0N 126.0W"},
    {"value": "52.5_235.0", "label": "52.5N 125.0W"},
    {"value": "52.0_236.0", "label": "52.0N 124.0W"},
    {"value": "51.5_237.5", "label": "51.5N 122.5W"},
    {"value": "51.0_239.0", "label": "51.0N 121.0W"},
    {"value": "50.5_239.5", "label": "50.5N 120.5W"},
    {"value": "50.0_240.0", "label": "50.0N 120.0W"},
    {"value": "49.5_240.0", "label": "49.5N 120.0W"},
    {"value": "49.0_240.0", "label": "49.0N 120.0W"},
    {"value": "48.5_240.0", "label": "48.5N 120.0W"},
    {"value": "48.0_240.0", "label": "48.0N 120.0W"},
    {"value": "47.5_240.0", "label": "47.5N 120.0W"},
    {"value": "47.0_239.5", "label": "47.0N 120.5W"},
    {"value": "46.5_239.5", "label": "46.5N 120.5W"},
    {"value": "46.0_239.0", "label": "46.0N 121.0W"},
    {"value": "45.5_239.0", "label": "45.5N 121.0W"},
    {"value": "45.0_239.0", "label": "45.0N 121.0W"},
    {"value": "44.5_239.0", "label": "44.5N 121.0W"},
    {"value": "44.0_239.0", "label": "44.0N 121.0W"},
    {"value": "43.5_238.5", "label": "43.5N 121.5W"},
    {"value": "43.0_238.5", "label": "43.0N 121.5W"},
    {"value": "42.5_238.5", "label": "42.5N 121.5W"},
    {"value": "42.0_239.0", "label": "42.0N 121.0W"},
    {"value": "41.5_239.0", "label": "41.5N 121.0W"},
    {"value": "41.0_239.5", "label": "41.0N 120.5W"},
    {"value": "40.5_240.0", "label": "40.5N 120.0W"},
    {"value": "40.0_240.5", "label": "40.0N 119.5W"},
    {"value": "39.5_241.0", "label": "39.5N 119.0W"},
    {"value": "39.0_241.5", "label": "39.0N 118.5W"},
    {"value": "38.5_242.0", "label": "38.5N 118.0W"},
    {"value": "38.0_242.5", "label": "38.0N 117.5W"},
    {"value": "37.5_242.5", "label": "37.5N 117.5W"},
    {"value": "37.0_243.0", "label": "37.0N 117.0W"},
    {"value": "36.5_243.0", "label": "36.5N 117.0W"},
    {"value": "36.0_243.5", "label": "36.0N 116.5W"},
    {"value": "35.5_244.0", "label": "35.5N 116.0W"},
    {"value": "35.0_244.5", "label": "35.0N 115.5W"},
    {"value": "34.5_245.0", "label": "34.5N 115.0W"},
    {"value": "34.0_246.5", "label": "34.0N 113.5W"},
    {"value": "33.5_247.5", "label": "33.5N 112.5W"},
    {"value": "33.0_248.0", "label": "33.0N 112.0W"},
    {"value": "32.5_248.0", "label": "32.5N 112.0W"},
    {"value": "32.0_248.0", "label": "32.0N 112.0W"},
    {"value": "31.5_248.5", "label": "31.5N 111.5W"},
    {"value": "31.0_248.5", "label": "31.0N 111.5W"},
    {"value": "30.5_249.0", "label": "30.5N 111.0W"},
    {"value": "30.0_249.5", "label": "30.0N 110.5W"},
    {"value": "29.5_249.5", "label": "29.5N 110.5W"},
    {"value": "29.0_250.0", "label": "29.0N 110.0W"},
    {"value": "28.5_250.0", "label": "28.5N 110.0W"},
    {"value": "28.0_250.5", "label": "28.0N 109.5W"},
    {"value": "27.5_250.5", "label": "27.5N 109.5W"},
    {"value": "27.0_251.0", "label": "27.0N 109.0W"},
    {"value": "26.5_251.0", "label": "26.5N 109.0W"},
    {"value": "26.0_251.5", "label": "26.0N 108.5W"},
    {"value": "25.5_251.5", "label": "25.5N 108.5W"},
    {"value": "25.0_252.0", "label": "25.0N 108.0W"},
]

interior_west = [
    {"value": "49.0_246.0", "label": "49.0N 114.0W"},
    {"value": "48.5_246.5", "label": "48.5N 113.5W"},
    {"value": "48.0_247.0", "label": "48.0N 113.0W"},
    {"value": "47.5_247.0", "label": "47.5N 113.0W"},
    {"value": "47.0_247.5", "label": "47.0N 112.5W"},
    {"value": "46.5_247.5", "label": "46.5N 112.5W"},
    {"value": "46.0_247.5", "label": "46.0N 112.5W"},
    {"value": "45.5_247.5", "label": "45.5N 112.5W"},
    {"value": "45.0_248.0", "label": "45.0N 112.0W"},
    {"value": "44.5_248.5", "label": "44.5N 111.5W"},
    {"value": "44.0_249.5", "label": "44.0N 110.5W"},
    {"value": "43.5_250.0", "label": "43.5N 110.0W"},
    {"value": "43.0_250.5", "label": "43.0N 109.5W"},
    {"value": "42.5_251.0", "label": "42.5N 109.0W"},
    {"value": "42.0_251.5", "label": "42.0N 108.5W"},
    {"value": "41.5_252.5", "label": "41.5N 107.5W"},
    {"value": "41.0_253.0", "label": "41.0N 107.0W"},
    {"value": "40.5_253.0", "label": "40.5N 107.0W"},
    {"value": "40.0_252.5", "label": "40.0N 107.5W"},
    {"value": "39.5_252.5", "label": "39.5N 107.5W"},
    {"value": "39.0_253.0", "label": "39.0N 107.0W"},
    {"value": "38.5_252.5", "label": "38.5N 107.5W"},
    {"value": "38.0_252.0", "label": "38.0N 108.0W"},
    {"value": "37.5_252.0", "label": "37.5N 108.0W"},
    {"value": "37.0_253.0", "label": "37.0N 107.0W"},
    {"value": "36.5_253.0", "label": "36.5N 107.0W"},
    {"value": "36.0_252.5", "label": "36.0N 107.5W"},
    {"value": "35.5_252.0", "label": "35.5N 108.0W"},
    {"value": "35.0_251.5", "label": "35.0N 108.5W"},
    {"value": "34.5_251.5", "label": "34.5N 108.5W"},
    {"value": "34.0_252.0", "label": "34.0N 108.0W"},
    {"value": "33.5_251.5", "label": "33.5N 108.5W"},
    {"value": "33.0_252.0", "label": "33.0N 108.0W"},
    {"value": "32.5_251.5", "label": "32.5N 108.5W"},
    {"value": "32.0_251.5", "label": "32.0N 108.5W"},
    {"value": "31.5_251.5", "label": "31.5N 108.5W"},
]

west_wrf_interior = [
    {"value": "49.0_246.0", "label": "49.0N 114.0W"},
    {"value": "48.5_246.5", "label": "48.5N 113.5W"},
    {"value": "48.0_247.0", "label": "48.0N 113.0W"},
    {"value": "47.5_247.0", "label": "47.5N 113.0W"},
    {"value": "47.0_247.5", "label": "47.0N 112.5W"},
    {"value": "46.5_247.5", "label": "46.5N 112.5W"},
    {"value": "46.0_247.5", "label": "46.0N 112.5W"},
    {"value": "45.5_247.5", "label": "45.5N 112.5W"},
    {"value": "45.0_248.0", "label": "45.0N 112.0W"},
    {"value": "44.5_248.5", "label": "44.5N 111.5W"},
    {"value": "44.0_249.5", "label": "44.0N 110.5W"},
    {"value": "43.5_250.0", "label": "43.5N 110.0W"},
    {"value": "43.0_250.0", "label": "43.0N 110.0W"},
    {"value": "42.5_250.0", "label": "42.5N 110.0W"},
    {"value": "42.0_250.0", "label": "42.0N 110.0W"},
    {"value": "41.5_250.0", "label": "41.5N 110.0W"},
    {"value": "41.0_250.0", "label": "41.0N 110.0W"},
    {"value": "40.5_250.0", "label": "40.5N 110.0W"},
    {"value": "40.0_250.0", "label": "40.0N 110.0W"},
    {"value": "39.5_250.0", "label": "39.5N 110.0W"},
    {"value": "39.0_250.0", "label": "39.0N 110.0W"},
    {"value": "38.5_250.0", "label": "38.5N 110.0W"},
    {"value": "38.0_250.0", "label": "38.0N 110.0W"},
    {"value": "37.5_250.0", "label": "37.5N 110.0W"},
    {"value": "37.0_250.0", "label": "37.0N 110.0W"},
    {"value": "36.5_250.0", "label": "36.5N 110.0W"},
    {"value": "36.0_250.0", "label": "36.0N 110.0W"},
    {"value": "35.5_250.0", "label": "35.5N 110.0W"},
    {"value": "35.0_250.0", "label": "35.0N 110.0W"},
    {"value": "34.5_250.0", "label": "34.5N 110.0W"},
    {"value": "34.0_250.0", "label": "34.0N 110.0W"},
    {"value": "33.5_250.0", "label": "33.5N 110.0W"},
    {"value": "33.0_250.0", "label": "33.0N 110.0W"},
    {"value": "32.5_250.0", "label": "32.5N 110.0W"},
    {"value": "32.0_250.0", "label": "32.0N 110.0W"},
    {"value": "31.5_250.0", "label": "31.5N 110.0W"},
]


class WestCoastIVTMagnitudePlumes(TethysDashPlugin):
    name = "cw3e_west_coast_ivt_magnitude_plumes"
    tags = [
        "cw3e",
        "ar",
        "plumes",
        "magnitude",
        "ivt",
    ]
    description = "Diagrams that represent the integrated water vapor transport (IVT) magnitude forecast from each of the GEFS ensemble models (thin gray lines), the unperturbed GEFS control forecast (black line), the ensemble mean (green line), and plus or minus one standard deviation from the ensemble mean (red line (+), blue line (-), and gray shading). More information can be found at https://cw3e.ucsd.edu/iwv-and-ivt-forecasts/"
    args = {
        "date": "date",
        "visualization": ["Map", "Plot"],
        "model": [
            {
                "value": "GEFS",
                "label": "GEFS",
                "sub_args": {
                    "forecast_length": [
                        {"value": "7", "label": "7 Days"},
                        {"value": "10", "label": "10 Days"},
                        {"value": "16", "label": "16 Days"},
                    ],
                    "transect_location": [
                        {
                            "value": "coast",
                            "label": "Coastal",
                            "sub_args": {"location": coastal_locations},
                        },
                        {
                            "value": "foothills",
                            "label": "Foothills",
                            "sub_args": {"location": foothill_locations},
                        },
                        {
                            "value": "inland",
                            "label": "Inland",
                            "sub_args": {"location": inland_locations},
                        },
                        {
                            "value": "intwest",
                            "label": "Interior West",
                            "sub_args": {"location": interior_west},
                        },
                    ],
                },
            },
            {
                "value": "ECMWF",
                "label": "ECMWF EPS",
                "sub_args": {
                    "forecast_length": [
                        {"value": "7", "label": "7 Days"},
                        {"value": "10", "label": "10 Days"},
                        {"value": "16", "label": "16 Days"},
                    ],
                    "transect_location": [
                        {
                            "value": "coast",
                            "label": "Coastal",
                            "sub_args": {"location": coastal_locations},
                        },
                        {
                            "value": "foothills",
                            "label": "Foothills",
                            "sub_args": {"location": foothill_locations},
                        },
                        {
                            "value": "inland",
                            "label": "Inland",
                            "sub_args": {"location": inland_locations},
                        },
                        {
                            "value": "intwest",
                            "label": "Interior West",
                            "sub_args": {"location": interior_west},
                        },
                    ],
                },
            },
            {
                "value": "GEFS_ECMWF",
                "label": "GEFS & ECMWF EPS",
                "sub_args": {
                    "forecast_length": [
                        {"value": "7", "label": "7 Days"},
                        {"value": "10", "label": "10 Days"},
                        {"value": "16", "label": "16 Days"},
                    ],
                    "transect_location": [
                        {
                            "value": "coast",
                            "label": "Coastal",
                            "sub_args": {"location": coastal_locations},
                        },
                        {
                            "value": "foothills",
                            "label": "Foothills",
                            "sub_args": {"location": foothill_locations},
                        },
                        {
                            "value": "inland",
                            "label": "Inland",
                            "sub_args": {"location": inland_locations},
                        },
                        {
                            "value": "intwest",
                            "label": "Interior West",
                            "sub_args": {"location": interior_west},
                        },
                    ],
                },
            },
            {
                "value": "WWRF",
                "label": "West-WRF",
                "sub_args": {
                    "forecast_length": [
                        {"value": "7", "label": "7 Days"},
                    ],
                    "transect_location": [
                        {
                            "value": "coast",
                            "label": "Coastal",
                            "sub_args": {"location": coastal_locations},
                        },
                        {
                            "value": "foothills",
                            "label": "Foothills",
                            "sub_args": {"location": foothill_locations},
                        },
                        {
                            "value": "inland",
                            "label": "Inland",
                            "sub_args": {"location": inland_locations},
                        },
                        {
                            "value": "intwestWWRF",
                            "label": "Interior West",
                            "sub_args": {"location": west_wrf_interior},
                        },
                    ],
                },
            },
            {
                "value": "WWRF_GEFS_ECMWF",
                "label": "West-WRF, GEFS, & ECMWF",
                "sub_args": {
                    "forecast_length": [
                        {"value": "7", "label": "7 Days"},
                    ],
                    "transect_location": [
                        {
                            "value": "coast",
                            "label": "Coastal",
                            "sub_args": {"location": coastal_locations},
                        },
                        {
                            "value": "foothills",
                            "label": "Foothills",
                            "sub_args": {"location": foothill_locations},
                        },
                        {
                            "value": "inland",
                            "label": "Inland",
                            "sub_args": {"location": inland_locations},
                        },
                        {
                            "value": "intwestWWRF",
                            "label": "Interior West",
                            "sub_args": {"location": west_wrf_interior},
                        },
                    ],
                },
            },
        ],
    }
    group = "CW3E"
    label = "West Coast IVT Magnitude Plumes"
    type = "image"
    attribution = "CW3E"

    def __init__(self, visualization, model, metadata=None, **kwargs):
        # store important kwargs
        self.visualization = visualization
        self.model = model
        self.forecast_length = kwargs.get("model.forecast_length")
        self.transect_location = kwargs.get("model.transect_location")
        self.location = kwargs.get("model.transect_location.location")

        # Pass kwargs through so the base class parses/sets the "date" arg.
        super().__init__(metadata=metadata, **kwargs)

    def run(self):
        transect = self.transect_location
        if transect == "intwestWWRF":
            transect = "intwest"

        # The location map has no v1 product; keep it on the legacy URL.
        if self.visualization == "Map":
            return (
                f"{BASE_URL}/gefs/images/Plume_maps/"
                f"Plume_maps_{transect}_{self.location}.png"
            )

        # West-WRF plume models have no v1 product; keep them on the legacy URL.
        if self.model in LEGACY_MODEL_BASES:
            base = LEGACY_MODEL_BASES[self.model]
            return (
                f"{BASE_URL}/{base}_IVTPlume_"
                f"{self.forecast_length}_{transect}_{self.location}.png"
            )

        # v1 scheme for GEFS / ECMWF / GEFS & ECMWF.
        model_info = NEW_SCHEME_MODELS[self.model]
        model = model_info["code"]
        interval = model_info["cycle_interval"]
        location = self._location_segment()
        forecast_hour = f"F{int(self.forecast_length) * 24:03d}"

        if self.date == "latest":
            return self._resolve_latest_url(model, interval, location, forecast_hour)

        # Validate the requested run cycle for the selected model.
        if self.date.hour % interval != 0:
            valid = ", ".join(f"{h:02d}Z" for h in range(0, 24, interval))
            raise VisualizationError(
                f"{self.model} model runs are only available at {valid}."
            )

        date_str = self.date.strftime("%Y%m%d%H")
        return self._build_url(model, location, date_str, forecast_hour)

    def _location_segment(self):
        """Build the "<lat>N_<lon>W" path component from the stored
        "<lat>_<lon360>" location value."""
        lat_str, lon360_str = self.location.split("_")
        lon_west = 360 - float(lon360_str)
        return f"{float(lat_str):.1f}N_{lon_west:.1f}W"

    def _build_url(self, model, location, date_str, forecast_hour):
        return (
            f"{BASE_URL}/ivt_ensembleplumes/v1/{model}/{location}/{date_str}/1/"
            f"ivt_ensembleplumes__v1__{model}__{location}__"
            f"{date_str}__1__{forecast_hour}.png"
        )

    def _resolve_latest_url(self, model, interval, location, forecast_hour):
        """Probe model run cycles backwards to find the newest available run."""
        # Round the current time down to the nearest valid run cycle.
        now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
        cycle = now.replace(hour=(now.hour // interval) * interval)

        # Look back up to ~10 days worth of run cycles.
        for _ in range((10 * 24) // interval):
            date_str = cycle.strftime("%Y%m%d%H")
            url = self._build_url(model, location, date_str, forecast_hour)
            try:
                if requests.head(url, timeout=10).status_code == 200:
                    return url
            except requests.RequestException:
                # Site unreachable (e.g. a blocked IP); assume the most
                # recent cycle's image exists instead of probing every cycle.
                return url
            cycle -= timedelta(hours=interval)

        raise VisualizationError(
            f"No IVT plume image found for {self.model} "
            f"({location}, {forecast_hour}) in the last 10 days."
        )
