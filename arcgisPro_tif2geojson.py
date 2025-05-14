import os
import rasterio
import geopandas as gpd
import numpy as np
from rasterio.features import shapes
from shapely.geometry import shape

# 文件夹路径
input_folder = 'arcgis_input'
output_folder = 'arcgis_output'

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 获取水深文件
water_depth_files = [f for f in os.listdir(input_folder) if 'WaterDepth' in f and f.endswith('.tif')]

print("水深文件：", water_depth_files)

for water_depth_file in water_depth_files:
    print(f"处理水深文件：{water_depth_file}")

    # 构造完整的文件路径
    water_depth_path = os.path.join(input_folder, water_depth_file)

    try:
        # 读取水深的 .tif 文件
        with rasterio.open(water_depth_path) as water_depth_src:
            water_depth = water_depth_src.read(1)
            water_depth_transform = water_depth_src.transform


        # 使用 rasterio 的 shapes 方法，将栅格转换为矢量
        def raster_to_geojson(raster_data, transform, property_name):
            results = []
            for geom, val in shapes(raster_data, transform=transform):
                results.append({
                    'geometry': shape(geom),
                    'properties': {property_name: val}
                })
            return results


        # 转换水深数据
        water_depth_geojson = raster_to_geojson(water_depth, water_depth_transform, 'WaterDepth')

        # 创建 GeoDataFrame
        gdf = gpd.GeoDataFrame.from_features(water_depth_geojson)

        # 保存为 GeoJSON 文件
        output_file = os.path.join(output_folder, f'{os.path.splitext(water_depth_file)[0]}.geojson')
        gdf.to_file(output_file, driver='GeoJSON')

        print(f"GeoJSON 文件生成成功：{output_file}")

    except Exception as e:
        print(f"处理 {water_depth_file} 时发生错误：{e}")
