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

# 收集depth文件
file_groups = {}
for filename in os.listdir(input_folder):
    if filename.endswith('.tif') and "Depth" in filename:
        # 提取时间戳（假设时间戳在文件名的中间部分，可以根据实际情况调整）
        timestamp = filename.split('(')[1].split(')')[0]
        file_groups[timestamp] = filename

# 处理每个 depth 文件
for timestamp, depth_file in file_groups.items():
    depth_path = os.path.join(input_folder, depth_file)
    output_path = os.path.join(output_folder, f"{timestamp}_depth_only.geojson")

    features_list = []

    with rasterio.open(depth_path) as depth_src:
        depth_band = depth_src.read(1)

        # 创建掩膜，仅包括非空值
        mask = depth_band != depth_src.nodata

        # 获取形状和对应深度值
        polygons = features.shapes(depth_band, mask=mask, transform=depth_src.transform)

        # 坐标转换
        transformer = Transformer.from_crs(depth_src.crs, "EPSG:4326", always_xy=True)

        for polygon, depth_value in polygons:
            if depth_value:
                geom = shape(polygon)

                # 获取多边形坐标并转换为地理坐标系
                coordinates = [transformer.transform(x, y) for x, y in geom.exterior.coords]

                # 构建GeoJSON Feature
                feature = Feature(
                    geometry={"type": "Polygon", "coordinates": [coordinates]},
                    properties={"depth": float(depth_value)}
                )
                features_list.append(feature)

    # 构建 FeatureCollection
    feature_collection = FeatureCollection(features_list)

    # 写入输出文件
    with open(output_path, 'w') as f:
        json.dump(feature_collection, f, indent=4)

    print(f"Processed {timestamp} and saved to {output_path}")

print("所有 depth .tif 文件已处理完成。")
