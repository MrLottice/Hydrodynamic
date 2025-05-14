import os
import rasterio
import json
from rasterio import features
from shapely.geometry import shape, mapping
from geojson import Feature, FeatureCollection
from pyproj import Transformer

# 输入和输出文件夹路径
input_folder = 'input'
output_folder = 'output'

# 创建输出文件夹（如果不存在）
os.makedirs(output_folder, exist_ok=True)

# 收集文件并按时间戳分组
file_groups = {}
for filename in os.listdir(input_folder):
    if filename.endswith('.tif'):
        # 提取时间戳（假设时间戳在文件名的中间部分，可以根据实际情况调整）
        timestamp = filename.split('(')[1].split(')')[0]
        if timestamp not in file_groups:
            file_groups[timestamp] = {}
        if "Depth" in filename:
            file_groups[timestamp]['depth'] = filename
        elif "WSE" in filename:
            file_groups[timestamp]['wse'] = filename
        elif "Velocity" in filename:
            file_groups[timestamp]['velocity'] = filename

# 处理每组文件
for timestamp, files in file_groups.items():
    if 'depth' in files and 'wse' in files and 'velocity' in files:
        depth_path = os.path.join(input_folder, files['depth'])
        wse_path = os.path.join(input_folder, files['wse'])
        velocity_path = os.path.join(input_folder, files['velocity'])
        output_path = os.path.join(output_folder, f"{timestamp}_combined.geojson")

        features_list = []

        with rasterio.open(depth_path) as depth_src, rasterio.open(wse_path) as wse_src, rasterio.open(velocity_path) as velocity_src:
            depth_band = depth_src.read(1)
            wse_band = wse_src.read(1)
            velocity_band = velocity_src.read(1)

            mask = (depth_band != depth_src.nodata) & (wse_band != wse_src.nodata) & (velocity_band != velocity_src.nodata)

            polygons = features.shapes(depth_band, mask=mask, transform=depth_src.transform)

            transformer = Transformer.from_crs(depth_src.crs, "EPSG:4326", always_xy=True)

            for polygon, depth_value in polygons:
                if depth_value:
                    geom = shape(polygon)
                    # 获取对应的 WSE 和 Velocity 值
                    centroid = geom.centroid
                    row, col = depth_src.index(centroid.x, centroid.y)
                    wse_value = wse_band[row, col]
                    velocity_value = velocity_band[row, col]

                    lon, lat = transformer.transform(centroid.x, centroid.y)
                    coordinates = [transformer.transform(x, y) for x, y in geom.exterior.coords]

                    feature = Feature(
                        geometry={"type": "Polygon", "coordinates": [coordinates]},
                        properties={"depth": float(depth_value), "wse": float(wse_value), "velocity": float(velocity_value)}
                    )
                    features_list.append(feature)

        feature_collection = FeatureCollection(features_list)

        with open(output_path, 'w') as f:
            json.dump(feature_collection, f, indent=4)

        print(f"Processed {timestamp} and saved to {output_path}")

print("所有 .tif 文件已处理完成。")
