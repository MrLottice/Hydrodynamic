import win32com.client as win32
import time
import numpy as np
from osgeo import gdal, osr
import os


# 创建HEC-RAS Controller对象
try:
    hecras = win32.Dispatch("RAS66.HECRASController")
    print("HEC-RAS Controller 已成功连接！")
except Exception as e:
    print(f"连接失败：{e}")
    exit()

# 打开HEC-RAS项目文件
project_path = r"D:\HEC-RAS Flood Monitor\test12\test12\test12.prj"
hecras.Project_Open(project_path)
print("项目已打开：", project_path)

# .u01 文件的位置
u01_file_path = r"D:\HEC-RAS Flood Monitor\test12\test12\test12.u01"

# 定义修改的流量时间序列数据

# 设置流量数据
bc_line_1 = "BC_Line_1"
data_interval = 3600  # 设置时序数据的间隔时间(单位:秒)

#使用 Edit_BC 方法进行编辑
hecras.Edit_BC(bc_line_1, "Flow Hydrograph", data_interval)
print("成功设置流量数据")

# 设置模拟开始的时间,开始时间+时序数据的时间 包含 后续的计算参数设置的时间
start_time = "2008-01-01 00:00"

# 添加流量时间序列数据
flow_data = [0, 400, 800, 1200, 1600, 2000, 2400, 2000, 1500, 800, 400, 0]

# 例如，尝试使用该方法并捕获可能的错误
try:
    hecras.Edit_UnsteadyFlowData(bc_line_1, flow_data)
except Exception as e:
    print(f"发生错误: {e}")

print("成功添加流量时间序列数据")

# 设置EG坡度（分配流量的坡度值）
eg_slope_value = 0.001

# 设置EG坡度以分配流量
hecras.Set_EG_Slope_DistributeFlow(bc_line_1, eg_slope_value)
print("BCLine1参数设置成功")

# # 设置边界线名称
# bc_line_name_2 = "BC_Line_2"
#
# # 设置正常深度
# hecras.Set_BoundaryCondition(bc_line_name_2, "Normal Depth")
#
# # 设置摩擦坡度
# friction_slope_value = 0.001
# hecras.Set_FrictionSlope(bc_line_name_2, friction_slope_value)
print("BCLine2参数设置成功")


# ====================================================================================================
#                                      Unsteady Flow Analysis部分
# ====================================================================================================

# # 设置要运行的程序
# hecras.Set_ProgramsToRun("Geometry Preprocessor")
# hecras.Add_ProgramToRun("Unsteady Flow Simulation")
#
# # 设置模拟的开始和结束时间(必须与与流量数据种设置的时间吻合)
# start_time = "2008-01-01 00:00"  # 开始时间
# end_time = "2008-01-01 12:00"    # 结束时间
# hecras.Set_SimulationStartTime(start_time)
# hecras.Set_SimulationEndTime(end_time)
#
# # 计算参数设置
# computation_interval = 600  # 计算间隔，单位为秒
# hydrograph_output_interval = 600  # 水文图输出间隔，单位为秒
# mapping_output_interval = 600  # 映射输出间隔，单位为秒
# detailed_output_interval = 600  # 详细输出间隔，单位为秒
#
# hecras.Set_ComputationInterval(computation_interval)
# hecras.Set_HydrographOutputInterval(hydrograph_output_interval)
# hecras.Set_MappingOutputInterval(mapping_output_interval)
# hecras.Set_DetailedOutputInterval(detailed_output_interval)

# ====================================================================================================
#                                                计算部分
# ====================================================================================================

# 开始计算
hecras.ComputeStartedFromController()

# 检查计算状态，使用循环等待计算完成
while True:
    # 检查当前计算状态
    status = hecras.Get_SimulationStatus()

    if status == 0:  # 计算成功
        print("计算已成功完成。")
        break
    elif status < 0:  # 计算失败
        error_message = hecras.Get_ErrorMessage()
        print(f"计算失败，错误代码: {status}，错误信息: {error_message}")
        break
    else:
        print("计算进行中...")
        time.sleep(5)  # 等待5秒后再检查

# ====================================================================================================
#                                                导出计算结果
# ====================================================================================================
# 获取二维流域的水位结果
time_steps, stage_results = hecras.Output2D_GetStage(two_d_area_name)

# 设置输出目录
output_directory = r"D:\水动力模型MIKE\input"
os.makedirs(output_directory, exist_ok=True)  # 创建输出目录（如果不存在）

# 遍历每个时间步并导出为.tif文件
for i, stage_array in enumerate(stage_results):
    # 假设结果是一个numpy数组（根据你的实际数据格式调整）
    stage_array = np.array(stage_array)

    # 设置输出.tif文件路径
    output_tif_path = os.path.join(output_directory, f"stage_output_time_{i}.tif")

    # 创建GeoTIFF文件
    driver = gdal.GetDriverByName('GTiff')
    rows, cols = stage_array.shape
    out_ds = driver.Create(output_tif_path, cols, rows, 1, gdal.GDT_Float32)

    # 设置投影和地理信息（根据你的数据设置）
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)  # 例：WGS 84
    out_ds.SetProjection(srs.ExportToWkt())

    # 写入数据
    out_ds.GetRasterBand(1).WriteArray(stage_array)

    # 关闭数据集
    out_ds.FlushCache()
    out_ds = None

    print(f"水位数据已成功导出为 {output_tif_path}")

# 关闭项目
hecras.Project_Close()