import rasterio
import json
from rasterio import features
from shapely.geometry import shape, mapping
from geojson import Feature, FeatureCollection

# 打开 GeoTIFF 文件
with rasterio.open('Depth (01SEP2008 15 00 00).Terrain.gc.tif') as src:
    # 读取数据
    band = src.read(1)

    # 掩膜掉无效数据
    mask = band != src.nodata

    # 将栅格数据转换为矢量数据（多边形）
    polygons = features.shapes(band, mask=mask, transform=src.transform)

    # 创建空的 GeoJSON Feature 列表
    features_list = []

    for polygon, value in polygons:
        # 仅添加有效的水深值区域
        if value:
            # 将栅格多边形转换为 Shapely 形状
            geom = shape(polygon)

            # 创建一个 GeoJSON 面 Feature
            feature = Feature(geometry=mapping(geom), properties={"depth": float(value)})

            # 添加到 Feature 列表中
            features_list.append(feature)

    # 创建一个 FeatureCollection
    feature_collection = FeatureCollection(features_list)

    # 使用 json 模块将 FeatureCollection 转换为 JSON 字符串
    geojson_str = json.dumps(feature_collection)

    # 保存为 GeoJSON 文件
    with open('output/output.geojson', 'w') as f:
        f.write(geojson_str)
