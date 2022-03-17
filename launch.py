# -*- coding: utf-8 -*-
# File  : start_for_windows_10.py
# Author: bilibili_花花花花花歌
# Date  : 2021-08-13 22:13

# 获取当前位置
import os
from re import T
import sys
import shutil
import msvcrt

from components.Three_D_PoseBaseline_vmd.api import run as td_vmd_run
from components.FCRN_DepthPrediction_vmd.tensorflow.api import run as fc_vmd_run
from components.Three_D_PoseBaseline_multi.applications.api import run as td_mutil_run

os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'

# 程序工作目录
work_dir = os.getcwd()
# 项目所在磁盘
project_disk_local = work_dir.split(":")[0].upper()


def press_any_key_exit(msg):
    print(msg)
    while True:
        if not msvcrt.getch():
            pass
        else:
            break
    sys.exit()


# 检测数据完整性
def check_data():
    # 在运行本程序之前，请先下载data.zip，并解压到项目根目录
    if not os.path.isdir(os.path.join(os.getcwd(), "data/")):
        print("警告：在运行本程序之前，请先下载data.zip，并解压到项目根目录")
        return False
    if not os.path.isdir(os.path.join(os.getcwd(), "utils/")):
        print("警告：在运行本程序之前，请先下载utils.zip，并解压到项目根目录")
        return False
    return True


# 检测视频路径
def check_video_name(video_path):
    # 检测视频文件名称
    video_name = video_path.split("\\")[-1].split(".")[0]
    if video_name.isdigit() and len(video_name) == 12:
        print("> 错误：文件名非法，不可为12位纯数字：" + video_name)
        return False
    # 检测是否位于不同磁盘
    video_disk_local = video_path.split(":")[0].upper()
    if video_disk_local != project_disk_local:
        print("> 错误：请确保本程序与视频同属于一个磁盘内。")
        return False
    return True

def main():
    warm = input("警告：运行该脚本将删除上一次本视频解析结果，请做好备份。【回车继续】")
    video_path = ""

    # 验证输入视频路径合法性
    while True:
        video_path = input("> 请输入视频路径：")
        if len(video_path) == 0:
            continue
        
        # 将视频路径转化为绝对路径
        video_path = os.path.abspath(video_path.replace("\"", ""))

        if not check_video_name(video_path):
            continue
        break
    
    
    is_custom = input("> 设置是否以自定义模式运行（yes/no）【默认no】：") or "no"
    custom = False if is_custom == "no" else True

    # 参数设定
    if custom:
        is_debug = input("> 是否需要显示详细调试信息（yes/no/warn）【默认no】：") or "no"
        depthPrediction_vmd_depth_interval = input(
            "设置深度间隔。越小，结果越清晰。【默认10】：") or "10"
        baseline_multi_center_xy_scale = input("设置X、Y轴贴图比例【默认30】：") or "30"
        baseline_multi_center_z_scale = input("设置z轴贴图比例【默认2】：") or "2"
        baseline_multi_global_x_angle = input(
            "设置三维转换后，X轴上的全局角度/坡度（-180到180）【默认15】：") or "15"
        baseline_multi_center_decimation_move = input(
            "设置中心采样偏移（center decimation move）【默认0】：") or "0"
        baseline_multi_ik_decimation_move = input(
            "设置IK采样偏移（IK decimation move）【默认1.5】：") or "1.5"
        baseline_multi_decimation_angle = input(
            "设置采样角度（decimation angle）(-180 到 180, 整数)【默认10】：") or "10"
        baseline_multi_is_alignment = input(
            "设置是否对齐（Alignment）（yes/no/warn）【默认yes】：") or "yes"
        baseline_multi_is_ik = input(
            "设置是否让输出的vmd文件带有IK/FK foot setting（yes/no）【默认yes】：") or "yes"
        baseline_multi_heel_position = input(
            "设置脚跟在Y轴上的位置，即脚跟和地面之间的距离）【默认0】：") or "0"
    else:
        is_debug = "no"
        depthPrediction_vmd_depth_interval = "10"
        baseline_multi_center_xy_scale = "30"
        baseline_multi_center_z_scale = "2"
        baseline_multi_global_x_angle = "15"
        baseline_multi_center_decimation_move = "0"
        baseline_multi_ik_decimation_move = "1.5"
        baseline_multi_decimation_angle = "10"
        baseline_multi_is_alignment = "yes"
        baseline_multi_is_ik = "yes"
        baseline_multi_heel_position = "0"

    # 设置日志级别
    if is_debug == "yes":
        log_verbose = "3"
    elif is_debug == "warn":
        log_verbose = "1"
    else:
        log_verbose = "2"


    # 需要解析视频的所在目录
    video_dir = os.path.dirname(video_path)
    # 结果文件路径
    result_path = os.path.join(video_dir, "result")

    # (清空)上次结果
    if os.path.exists(result_path):
        shutil.rmtree(result_path)
    os.makedirs(result_path)

    print("> 开始进行视频姿态识别")
    # OpenPose组件相关路径
    openpose_path = os.path.join(work_dir, "utils/openpose/bin/OpenPoseDemo.exe")
    openpose_write_json_path = os.path.join(video_dir, "_json")
    openpose_write_video_path = os.path.join(video_dir, "_openpose.avi")

    # 删除上次结果
    if os.path.exists(openpose_write_json_path):
        shutil.rmtree(openpose_write_json_path)
    os.makedirs(openpose_write_json_path)

    if os.path.exists(openpose_write_video_path):
        os.remove(openpose_write_video_path)

    # 运行组件
    os.chdir(os.path.join(work_dir, "utils/openpose"))
    cmd_part_1 = "{} --model_pose COCO --video {} --write_json {} --write_video {} --number_people_max 1 --net_resolution \"-1x240\"".format(openpose_path, video_path, openpose_write_json_path, openpose_write_video_path)
    os.system(cmd_part_1)
    os.chdir(work_dir)
    
    print("> 开始生成3D姿态平面数据")
    # 删除上次结果
    baseline_vmd_result_name = ""
    for file_name in os.listdir(video_dir):
        if "_json_3d_" in file_name:
            baseline_vmd_result_name = file_name
            baseline_vmd_result_path =  os.path.join(video_dir, baseline_vmd_result_name)
            shutil.rmtree(baseline_vmd_result_path)

    # 运行组件
    td_vmd_run(dropout=0.5, epochs=200, load=4874200, gif_fps=30, verbose=int(log_verbose), openpose=openpose_write_json_path)

    # 获取结果文件路径
    baseline_vmd_result_name = ""
    for file_name in os.listdir(video_dir):
        if "_json_3d_" in file_name:
            baseline_vmd_result_name = file_name

    if baseline_vmd_result_name == "":
        print("错误：未找到3d-pose-baseline-vmd组件生成结果，请检查上一步操作。")
        press_any_key_exit("按任意键退出...")
    else:
        baseline_vmd_result_path =  os.path.join(video_dir, baseline_vmd_result_name)

    print("> 开始进行姿态数据深度推定")

    # 运行组件
    fc_vmd_run(video_path=openpose_write_video_path, baseline_path=baseline_vmd_result_path, interval=int(depthPrediction_vmd_depth_interval), verbose=int(log_verbose))

    print("> 开始生成vmd动作文件")

    if baseline_multi_is_alignment == "no":
        baseline_multi_alignment = "0"
    else:
        baseline_multi_alignment = "1"

    if baseline_multi_is_ik == "no":
        baseline_multi_ik_flag = "0"
    else:
        baseline_multi_ik_flag = "1"

    # 运行组件
    td_mutil_run(target=baseline_vmd_result_path, 
		verbose=int(log_verbose), 
		centerxy=int(baseline_multi_center_xy_scale), 
		centerz=float(baseline_multi_center_z_scale),
		xangle=int(baseline_multi_global_x_angle), 
		ddecimation=int(baseline_multi_decimation_angle),
		mdecimation=float(baseline_multi_center_decimation_move),
		idecimation=float(baseline_multi_ik_decimation_move), 
		alignment=int(baseline_multi_alignment),
		legik=int(baseline_multi_ik_flag),
		heelpos=float(baseline_multi_heel_position))

    # 获取结果文件路径
    result_vmd_name = ""
    result_depth_gif_path = ""
    result_smooth_gif_path = ""

    for file_name in os.listdir(baseline_vmd_result_path):
        if "output_" in file_name:
            result_vmd_name = file_name

    if result_vmd_name == "":
        print("错误：未找到VMD-3d-pose-baseline-multi组件生成结果，请检查上一步操作。")
        press_any_key_exit("按任意键退出...")
    else:
        result_vmd_path =  os.path.join(baseline_vmd_result_path, result_vmd_name)
        result_smooth_gif_path = os.path.join(baseline_vmd_result_path, "movie_depth.gif")
        result_depth_gif_path = os.path.join(baseline_vmd_result_path, "movie_smoothing.gif")

    # 复制结果文件
    shutil.copy(result_vmd_path, result_path)
    shutil.copy(result_depth_gif_path, result_path)
    shutil.copy(result_smooth_gif_path, result_path)

    os.system("cls")
    print("视频解析完成！")
    print("动作捕捉结果文件路径：" + result_path)

    os.system("explorer.exe {}".format(result_path))


if __name__ == "__main__":
    if check_data():
        main()

