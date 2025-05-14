from osgeo import gdal

# 输入栅格文件列表
input_files = [
    r"D:\视频测流\ultralytics-main\clip1.tif"
]

# 输出VRT文件路径
output_vrt = r"D:\视频测流\ultralytics-main\output/output.vrt"

# 创建VRT文件
gdal.BuildVRT(output_vrt, input_files)

print(f"VRT file created at {output_vrt}")
