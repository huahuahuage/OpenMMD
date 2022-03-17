# OpenMMD
OpenMMD可以称为OpenPose+MikuMikuDance（MMD），是一个基于OpenPose的深度学习项目，可以直接将真人视频动作转换为MMD的VMD模型文件（即Miku、Anmicius）。

简而言之，你录制了一段带有人体运动的视频，通过这个项目，你可以提取到一个与你在视频中的动作相同的模型文件，且无需专业动捕设备。

## 运行要求
* 操作系统：windows 8.0 及以上
* python 版本 >= 3.6
* NVIDIA graphics card with at least 1.6 GB available 
* At least 2.5 GB of free RAM memory for BODY_25 model or 2 GB for COCO model (assuming cuDNN installed).  
* Highly recommended: cuDNN

## 安装与使用
* 下载 data.zip 和 utils.zip，并解压到项目根目录([百度网盘]())。
* pip install -r requirements.txt
* python launch.py

## 项目相关引用
* [peterljq/OpenMMD](https://github.com/peterljq/OpenMMD)

OpenMMD is an OpenPose-based application that can convert real-person videos to the motion files (.vmd) which directly implement the 3D model (e.g. Miku, Anmicius) animated movies.


* [CMU-Perceptual-Computing-Lab/openpose](https://github.com/CMU-Perceptual-Computing-Lab/openpose)

OpenPose has represented the first real-time multi-person system to jointly detect human body, hand, facial, and foot keypoints (in total 135 keypoints) on single images.

It is authored by Ginés Hidalgo, Zhe Cao, Tomas Simon, Shih-En Wei, Yaadhav Raaj, Hanbyul Joo, and Yaser Sheikh. It is maintained by Ginés Hidalgo and Yaadhav Raaj. OpenPose would not be possible without the CMU Panoptic Studio dataset. We would also like to thank all the people who has helped OpenPose in any way.


* [una-dinosauria/3d-pose-baseline](https://github.com/una-dinosauria/3d-pose-baseline)

This is the code for the paper

Julieta Martinez, Rayat Hossain, Javier Romero, James J. Little. A simple yet effective baseline for 3d human pose estimation. In ICCV, 2017. [https://arxiv.org/pdf/1705.03098.pdf](https://arxiv.org/pdf/1705.03098.pdf).

The code in this repository was mostly written by Julieta Martinez, Rayat Hossain and Javier Romero.


* [iro-cp/FCRN-DepthPrediction](https://github.com/iro-cp/FCRN-DepthPrediction)

Deeper Depth Prediction with Fully Convolutional Residual Networks

