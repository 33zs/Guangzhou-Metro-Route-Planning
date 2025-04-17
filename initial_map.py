import requests
import time
import numpy as np

import math
import matplotlib.colors as mcolors
import plotly.offline as py
import plotly.graph_objs as go
def initial_map():
    PI = math.pi

    # Function to transform latitude for coordinate conversion
    def _transformlat(coordinates):
        # Detailed transformation logic for latitude
        lng = coordinates[:, 0] - 105
        lat = coordinates[:, 1] - 35
        ret = -100 + 2 * lng + 3 * lat + 0.2 * lat * lat + \
              0.1 * lng * lat + 0.2 * np.sqrt(np.fabs(lng))
        ret += (20 * np.sin(6 * lng * PI) + 20 *
                np.sin(2 * lng * PI)) * 2 / 3
        ret += (20 * np.sin(lat * PI) + 40 *
                np.sin(lat / 3 * PI)) * 2 / 3
        ret += (160 * np.sin(lat / 12 * PI) + 320 *
                np.sin(lat * PI / 30.0)) * 2 / 3
        return ret

    # Function to transform longitude for coordinate conversion
    def _transformlng(coordinates):
        # Detailed transformation logic for longitude
        lng = coordinates[:, 0] - 105
        lat = coordinates[:, 1] - 35
        ret = 300 + lng + 2 * lat + 0.1 * lng * lng + \
              0.1 * lng * lat + 0.1 * np.sqrt(np.fabs(lng))
        ret += (20 * np.sin(6 * lng * PI) + 20 *
                np.sin(2 * lng * PI)) * 2 / 3
        ret += (20 * np.sin(lng * PI) + 40 *
                np.sin(lng / 3 * PI)) * 2 / 3
        ret += (150 * np.sin(lng / 12 * PI) + 300 *
                np.sin(lng / 30 * PI)) * 2 / 3
        return ret

    # Convert GCJ-02 coordinates to WGS-84
    def gcj02_to_wgs84(coordinates):
        """
        Convert GCJ-02 to WGS-84
        :param coordinates: numpy array of longitude and latitude in GCJ-02 coordinate system
        :returns: numpy array of longitude and latitude in WGS-84 coordinate system
        """
        ee = 0.006693421622965943
        a = 6378245
        lng = coordinates[:, 0]
        lat = coordinates[:, 1]
        is_in_china = (lng > 73.66) & (lng < 135.05) & (lat > 3.86) & (lat < 53.55)
        _transform = coordinates[is_in_china]
        # Conversion logic
        dlat = _transformlat(_transform)
        dlng = _transformlng(_transform)
        radlat = _transform[:, 1] / 180 * PI
        magic = np.sin(radlat)
        magic = 1 - ee * magic * magic
        sqrtmagic = np.sqrt(magic)
        dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * PI)
        dlng = (dlng * 180.0) / (a / sqrtmagic * np.cos(radlat) * PI)
        mglat = _transform[:, 1] + dlat
        mglng = _transform[:, 0] + dlng
        coordinates[is_in_china] = np.array([
            _transform[:, 0] * 2 - mglng, _transform[:, 1] * 2 - mglat
        ]).T
        return coordinates

    # Convert BD-09 coordinates to GCJ-02
    def bd09_to_gcj02(coordinates):
        """
        Convert BD-09 to GCJ-02
        :param coordinates: numpy array of longitude and latitude in BD-09 coordinate system
        :returns: numpy array of longitude and latitude in GCJ-02 coordinate system
        """
        x_pi = PI * 3000 / 180
        x = coordinates[:, 0] - 0.0065
        y = coordinates[:, 1] - 0.006
        z = np.sqrt(x * x + y * y) - 0.00002 * np.sin(y * x_pi)
        theta = np.arctan2(y, x) - 0.000003 * np.cos(x * x_pi)
        lng = z * np.cos(theta)
        lat = z * np.sin(theta)
        coordinates = np.array([lng, lat]).T
        return coordinates

    # Convert BD-09 coordinates to WGS-84
    def bd09_to_wgs84(coordinates):
        """
        Convert BD-09 to WGS-84
        :param coordinates: numpy array of longitude and latitude in BD-09 coordinate system
        :returns: numpy array of longitude and latitude in WGS-84 coordinate system
        """
        return gcj02_to_wgs84(bd09_to_gcj02(coordinates))

    # Convert BD-09MC (Mercator) coordinates to BD-09
    def mercator_to_bd09(mercator):
        """
        Convert BD-09MC to BD-09
        :param mercator: numpy array of Mercator coordinates
        :returns: numpy array of longitude and latitude in BD-09 coordinate system
        """
        MCBAND = [12890594.86, 8362377.87, 5591021, 3481989.83, 1678043.12, 0]
        MC2LL = [[1.410526172116255e-08, 8.98305509648872e-06, -1.9939833816331,
                  200.9824383106796, -187.2403703815547, 91.6087516669843,
                  -23.38765649603339, 2.57121317296198, -0.03801003308653,
                  17337981.2],
                 [-7.435856389565537e-09, 8.983055097726239e-06, -0.78625201886289,
                  96.32687599759846, -1.85204757529826, -59.36935905485877,
                  47.40033549296737, -16.50741931063887, 2.28786674699375,
                  10260144.86],
                 [-3.030883460898826e-08, 8.98305509983578e-06, 0.30071316287616,
                  59.74293618442277, 7.357984074871, -25.38371002664745,
                  13.45380521110908, -3.29883767235584, 0.32710905363475,
                  6856817.37],
                 [-1.981981304930552e-08, 8.983055099779535e-06, 0.03278182852591,
                  40.31678527705744, 0.65659298677277, -4.44255534477492,
                  0.85341911805263, 0.12923347998204, -0.04625736007561,
                  4482777.06],
                 [3.09191371068437e-09, 8.983055096812155e-06, 6.995724062e-05,
                  23.10934304144901, -0.00023663490511, -0.6321817810242,
                  -0.00663494467273, 0.03430082397953, -0.00466043876332,
                  2555164.4],
                 [2.890871144776878e-09, 8.983055095805407e-06, -3.068298e-08,
                  7.47137025468032, -3.53937994e-06, -0.02145144861037,
                  -1.234426596e-05, 0.00010322952773, -3.23890364e-06,
                  826088.5]]

        x = np.abs(mercator[:, 0])
        y = np.abs(mercator[:, 1])
        coef = np.array([
            MC2LL[index] for index in
            (np.tile(y.reshape((-1, 1)), (1, 6)) < MCBAND).sum(axis=1)
        ])
        return converter(x, y, coef)

    # Helper function for conversion
    def converter(x, y, coef):
        x_temp = coef[:, 0] + coef[:, 1] * np.abs(x)
        x_n = np.abs(y) / coef[:, 9]
        y_temp = coef[:, 2] + coef[:, 3] * x_n + coef[:, 4] * x_n ** 2 + \
                 coef[:, 5] * x_n ** 3 + coef[:, 6] * x_n ** 4 + coef[:, 7] * x_n ** 5 + \
                 coef[:, 8] * x_n ** 6
        x[x < 0] = -1
        x[x >= 0] = 1
        y[y < 0] = -1
        y[y >= 0] = 1
        x_temp *= x
        y_temp *= y
        coordinates = np.array([x_temp, y_temp]).T
        return coordinates

    # Mapbox access token
    mapbox_access_token = (
        'pk.eyJ1IjoibHVrYXNtYXJ0aW5lbGxpIiwiYSI6ImNpem85dmhwazAy'
        'ajIyd284dGxhN2VxYnYifQ.HQCmyhEXZUTz3S98FMrVAQ'
    )
    layout = go.Layout(
        autosize=True,
        mapbox=dict(
            accesstoken=mapbox_access_token,
            center=dict(
                lat=23.12864583,  # Latitude of Guangzhou
                lon=113.2648325  # Longitude of Guangzhou
            ),
            pitch=0,
            zoom=10,
        ),
    )

    # Required metro lines and their colors
    required_lines = ['地铁1号线(西塱-广州东站)', '地铁2号线(嘉禾望岗-广州南站)', '地铁3号线(番禺广场-天河客运站)', '地铁3号线北延段(机场北(2号航站楼)-体育西路)']

    color = ('gold', 'blue', 'orange','orange')  # 可按需增加

    # Convert color name to RGBA format
    def convert_color_to_rgba(color_name, alpha):
        rgb = mcolors.to_rgb(color_name)
        return f"rgba({int(rgb[0] * 255)}, {int(rgb[1] * 255)}, {int(rgb[2] * 255)}, {alpha})"


    alpha = 1
    rgba_colors = [convert_color_to_rgba(color, alpha) for color in color]

    # Prepare data for map plotting
    data = []
    marked = set()
    cnt = 0

    # Retrieve station information
    null = None
    city_code = 257
    response = requests.get(f'http://map.baidu.com/?qt=bsi&c={city_code}&t={int(time.time() * 1000)}')
    station_info_json = eval(response.content)

    # Iterate over each metro line
    for line in station_info_json['content']:
        if line['line_name'] not in required_lines:
            continue
        uid = line['line_uid']
        if uid in marked:  # Skip reverse direction of the same line
            continue

        plots = []  # Stations' BD-09MC coordinates
        plots_name = []  # Stations' names

        # Extract coordinates and names
        for plot in line['stops']:
            plots.append([plot['x'], plot['y']])
            plots_name.append(plot['name'])

        # Convert coordinates to WGS-84
        plot_mercator = np.array(plots)
        plot_coordinates = bd09_to_wgs84(mercator_to_bd09(plot_mercator))  # 站台经纬度



        line_color = rgba_colors[required_lines.index(line['line_name'])]
        # Add line data for plotting
        data.append(
            go.Scattermapbox(
                lon=plot_coordinates[:, 0],
                lat=plot_coordinates[:, 1],
                mode='markers+lines+text',
                name=line['line_name'],
                text=plots_name,
                textposition='top right',
                marker=go.scattermapbox.Marker(
                    size=10,
                    color=line_color
                ),
                line=dict(color=line_color),
            )
        )
        # Create and display the map
    fig = dict(data=data, layout=layout)
    py.plot(fig, filename='static/Guangzhou_railway.html')

# initial_map()