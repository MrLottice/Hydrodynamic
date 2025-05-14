import os
import re


def convert_to_minutes(day_str, hour_str, minute_str):
    """将时间转换为以10为单位的文件名
    例如：
    15日 00:10 -> 10
    15日 00:20 -> 20
    15日 01:10 -> 70 (1小时10分钟 = 70分钟)
    15日 02:10 -> 130 (2小时10分钟 = 130分钟)
    """
    hours = int(hour_str)
    minutes = int(minute_str)
    total_minutes = hours * 60 + minutes  # 将小时转换为分钟后加上分钟数
    return total_minutes


def rename_files(directory):
    """批量重命名目录中的 GeoJSON 文件"""
    print(f"正在扫描目录: {directory}")
    print(f"目录是否存在: {os.path.exists(directory)}")
    
    for filename in os.listdir(directory):
        print(f"处理文件: {filename}")
        # 匹配新的文件名格式
        match = re.match(r'(\d{2})FEB2025 (\d{2}) (\d{2}) \d{2}_combined\.geojson', filename)
        if match:
            print(f"文件 {filename} 匹配成功")
            day, hour, minute = match.groups()
            new_name = f"{convert_to_minutes(day, hour, minute)}.geojson"
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_name)
            try:
                os.rename(old_path, new_path)
                print(f"重命名成功: {filename} -> {new_name}")
            except Exception as e:
                print(f"重命名失败: {str(e)}")
        else:
            print(f"文件 {filename} 不匹配正则表达式模式")


# 使用绝对路径
directory = os.path.abspath('output')
print(f"使用的完整路径: {directory}")
rename_files(directory)
