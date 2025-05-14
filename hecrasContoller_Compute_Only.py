import win32com.client as win32
import time

def format_flow_data(flow_data):
    """格式化流量数据，每个数据占8个字符，每行最多10个数据"""
    formatted = [str(item).rjust(8) for item in flow_data]
    lines = ["".join(formatted[i:i + 10]) for i in range(0, len(formatted), 10)]
    return "\n".join(lines)
 
def replace_flow_data_in_u01(file_path, flow_data_str):
    """替换 .u01 文件中的流量数据"""
    try:
        with open(file_path, 'r') as file:
            file_content = file.readlines()

        # 动态查找 Flow Hydrograph 数据的起始位置
        start_index = None
        for idx, line in enumerate(file_content):
            if "Flow Hydrograph" in line:
                start_index = idx + 1
                break

        if start_index is None:
            print("未找到 Flow Hydrograph 关键字，无法替换数据。")
            return

        end_index = start_index + flow_data_str.count("\n")  # 替换行数根据数据决定
        file_content[start_index:end_index] = [flow_data_str + "\n"]

        # 写回文件
        with open(file_path, 'w') as file:
            file.writelines(file_content)
        print("Flow Hydrograph 数据已成功替换！")
    except Exception as e:
        print(f"文件操作失败：{e}")

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
print("成功打开项目文件")

# 新的流量数据
new_flow_data = [
    300, 130, 160, 190, 220, 250, 220, 190, 150, 130,
    110, 89.286, 78.571, 67.857, 57.143, 46.429, 35.714, 25, 14.286, 3.571,
    2.857, 2.143, 1.429, 0.714, 0
]
formatted_flow_data = format_flow_data(new_flow_data)

# 修改 .u01 文件
u01_file_path = r"D:\HEC-RAS Flood Monitor\test12\test12\test12.u01"
replace_flow_data_in_u01(u01_file_path, formatted_flow_data)

# 开始计算
hecras.Compute_CurrentPlan()
print("开始计算...")

# 检查计算状态
complete_flag = 1
while complete_flag == 1:
    status = hecras.Compute_Complete()
    if not status:
        print("计算进行中...")
        time.sleep(5)
    else:
        print("计算完成！")
        complete_flag = 0

# 导出计算结果
plan_name = "Plan 01"  # 计算计划名称
file_name = r"D:\水动力模型MIKE\output_csv\output.csv"  # 输出文件路径
format_type = 0  # 输出为CSV格式

# 导出结果
hecras.Output_ComputationLevel_Export(plan_name, file_name, format_type)
print(f"计算结果已导出到 {file_name}")