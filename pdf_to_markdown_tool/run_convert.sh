#!/bin/bash

# 安装必要的软件包
sudo apt update
sudo apt install -y libgl1-mesa-glx

# 安装Python依赖
pip install -r requirements.txt

# 安装额外的Python包
pip install marker-pdf

# 设置环境变量
export HF_ENDPOINT=https://hf-mirror.com

# 运行Python脚本
python convert.py
