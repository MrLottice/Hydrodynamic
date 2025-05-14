import os
import re
from osgeo import gdal


def convert_to_minutes(hour_str, minute_str):
    """将小时和分钟转换为总分钟数"""
    hours = int(hour_str)
    minutes = int(minute_str)
    return hours * 60 + minutes


def rename_and_convert_files(directory):
    """批量重命名并转换坐标系"""
    for filename in os.listdir(directory):
        # 匹配文件名格式
        match = re.match(r'Depth \(\d{2}SEP2008 (\d{2}) (\d{2}) \d{2}\).Terrain.Terrain.liuyu.tif', filename)
        if match:
            hour, minute = match.groups()
            new_name = f"{convert_to_minutes(hour, minute)}.tif"

            old_path = os.path.join(directory, filename)
            temp_path = os.path.join(directory, f"temp_{new_name}")
            new_path = os.path.join(directory, new_name)

            # 检查是否已经存在同名文件
            if os.path.exists(new_path):
                print(f"File {new_name} already exists, skipping.")
                continue

            # 执行坐标系转换并保存到临时文件
            convert_projection(old_path, temp_path)

            # 将临时文件重命名为目标文件名
            os.rename(temp_path, new_path)
            print(f"Renamed and converted: {filename} -> {new_name}")


def convert_projection(input_tif, output_tif):
    """将坐标系从 EPSG:3857 转换为 EPSG:4326"""
    gdal.Warp(output_tif, input_tif, dstSRS='EPSG:4326')
    print(f"Converted projection: {input_tif} -> {output_tif}")


# 替换为你的目录路径
directory = 'input'
rename_and_convert_files(directory)
