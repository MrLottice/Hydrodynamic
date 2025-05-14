import rasterio
import numpy as np


def dem_tif_to_xyz(tif_path, xyz_path):
    # 打开tif文件
    with rasterio.open(tif_path) as src:
        # 读取数据
        data = src.read(1)
        # 获取NoData值
        nodata = src.nodata
        # 获取坐标转换参数
        transform = src.transform

        # 打开xyz文件准备写入
        with open(xyz_path, 'w') as xyz_file:
            # 遍历每个像素
            for row in range(data.shape[0]):
                for col in range(data.shape[1]):
                    # 计算像素中心的地理坐标
                    x, y = transform * (col, row)
                    # 获取像素值 (高程)
                    z = data[row, col]
                    # 写入xyz文件, 过滤掉NoData值的像素
                    if z != nodata:
                        xyz_file.write(f"{x} {y} {z}\n")


# 使用示例
tif_path = r'D:\水动力模型MIKE\only_river_dem.tif'
xyz_path = r'D:\水动力模型MIKE\output\only_river_dem.xyz'
dem_tif_to_xyz(tif_path, xyz_path)
