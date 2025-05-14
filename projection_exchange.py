import json
from pyproj import Transformer

# 创建一个转换器，假设原始投影坐标系为 EPSG:3857（Web Mercator），目标坐标系为 EPSG:4326（WGS84）
transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)

# 读取 GeoJSON 文件
with open('output/output.geojson', 'r') as f:
    geojson_data = json.load(f)

# 转换每个坐标
for feature in geojson_data['features']:
    coordinates = feature['geometry']['coordinates'][0]  # 获取多边形的坐标
    for i in range(len(coordinates)):
        lon, lat = transformer.transform(coordinates[i][0], coordinates[i][1])
        coordinates[i][0] = lon
        coordinates[i][1] = lat

# 保存转换后的 GeoJSON 文件
with open('output/output_converted.geojson', 'w') as f:
    json.dump(geojson_data, f, indent=4)
