from intake.source import base

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


class WestCoastIVTMagnitudePlumes(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "cw3e_west_coast_ivt_magnitude_plumes"
    visualization_tags = [
        "cw3e",
        "ar",
        "plumes",
        "magnitude",
        "ivt",
    ]
    visualization_description = "Diagrams that represent the integrated water vapor transport (IVT) magnitude forecast from each of the GEFS ensemble models (thin gray lines), the unperturbed GEFS control forecast (black line), the ensemble mean (green line), and plus or minus one standard deviation from the ensemble mean (red line (+), blue line (-), and gray shading). More information can be found at https://cw3e.ucsd.edu/iwv-and-ivt-forecasts/"
    visualization_args = {
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
    visualization_group = "CW3E"
    visualization_label = "West Coast IVT Magnitude Plumes"
    visualization_type = "image"

    def __init__(self, visualization, model, metadata=None, **kwargs):
        # store important kwargs
        self.visualization = visualization
        self.model = model
        self.forecast_length = kwargs.get("model.forecast_length")
        self.transect_location = kwargs.get("model.transect_location")
        self.location = kwargs.get("model.transect_location.location")

        super().__init__(metadata=metadata)

    def read(self):

        url_location = self.model
        if self.model == "GEFS":
            url_location = "gefs/IVT_Plumes/GEFS"
        elif self.model == "ECMWF":
            url_location = "ECMWF/IVT_Ensemble_Plumes/ECMWF"
        elif self.model == "GEFS_ECMWF":
            url_location = "ECMWF/IVT_Ensemble_Plumes/GEFS_ECMWF"
        elif self.model == "WWRF":
            url_location = "wwrf/ensemble/IVTPlumes/West-WRF"
        elif self.model == "WWRF_GEFS_ECMWF":
            url_location = "wwrf/ensemble/IVTPlumes/GEFS_ECMWF_West-WRF"

        if self.visualization == "Map":
            return f"https://cw3e.ucsd.edu/images/gefs/images/Plume_maps/Plume_maps_{self.transect_location}_{self.location}.png"

        if self.transect_location == "intwestWWRF":
            self.transect_location = "intwest"

        return f"https://cw3e.ucsd.edu/images/{url_location}_IVTPlume_{self.forecast_length}_{self.transect_location}_{self.location}.png"
