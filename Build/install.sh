#!/bin/bash
# 获取当前脚本的绝对路径
SCRIPT_DIR=$(dirname "$(realpath "$0")")
# 获取上级文件夹的上级文件夹路径
PARENT_DIR=$(dirname "$SCRIPT_DIR")

set -e  # 使脚本在遇到错误时立即退出
sudo apt-get update
sudo apt-get install wget libicu-dev vim -y

# 检查 .NET 环境
if command -v dotnet &>/dev/null; then
    echo ".NET 已安装"
    DOTNET_VERSION=$(dotnet --version)
    REQUIRED_VERSION="6.0"
    if [[ "$DOTNET_VERSION" != 6.* ]]; then
        echo ".NET 版本不符合要求，当前版本是 $DOTNET_VERSION，要求是 6.0.x"
    else
        echo ".NET 版本符合要求：$DOTNET_VERSION"
    fi
else
    # 检查 .NET SDK 是否已下载
    DOTNET_SDK_URL="https://download.visualstudio.microsoft.com/download/pr/12ee34e8-640c-400e-a6dc-4892b442df92/81d40fc98a5bbbfbafa4cc1ab86d6288/dotnet-sdk-6.0.427-linux-x64.tar.gz"
    DOTNET_SDK_FILE="dotnet-sdk-6.0.427-linux-x64.tar.gz"
    DOTNET_DIR="$HOME/.dotnet"

    echo ".NET 环境未检测到，正在检查 .NET SDK 文件是否已下载..."
    # 如果文件不存在，则下载
    if [ ! -f "$DOTNET_SDK_FILE" ]; then
        echo "未检测到 SDK 文件，正在下载 .NET SDK..."
        wget $DOTNET_SDK_URL -O $DOTNET_SDK_FILE
    else
        echo ".NET SDK 文件已经下载，跳过下载步骤"
    fi

    echo "正在安装 .NET 6.0 SDK..."
    # 创建安装目录并解压
    mkdir -p $DOTNET_DIR
    tar -zxf $DOTNET_SDK_FILE -C $DOTNET_DIR

    # 创建符号链接到已在 PATH 中的目录
    echo "安装完成，正在创建符号链接..."
    sudo ln -s $DOTNET_DIR/dotnet /usr/local/bin/dotnet
    
    # 删除下载的文件（如果安装成功）
    if command -v dotnet &> /dev/null; then
        echo ".NET SDK 安装成功，删除下载的文件..."
        rm -f $DOTNET_SDK_FILE
    else
        echo ".NET SDK 安装失败，停止执行脚本"
        exit 1
    fi

    echo "已将 DOTNET_ROOT 和 PATH 环境变量持久化，并已设置为 $DOTNET_DIR"
fi

# 检查 Python 环境
if command -v python3 &>/dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "Python 环境已安装：$PYTHON_VERSION ,推荐版本 Python 3.8.2 "
else
    echo "未检测到 Python 环境，正在安装 Python 3.8..."
    sudo apt-get install python3.8 python3.8-venv python3.8-dev python3-pip -y
    echo "Python 3.8 安装完成"
fi

# 获取当前目录
current_dir=$PWD

# 检查目标项目目录是否已存在
if [ -d "$PARENT_DIR/Build/restler-fuzzer" ]; then
    echo "restler-fuzzer 项目已存在，跳过克隆步骤..."
else
    # 克隆目标项目
    echo "正在克隆 restler-fuzzer 项目..."
    git clone https://github.com/microsoft/restler-fuzzer.git  $PARENT_DIR/Build/restler-fuzzer/
fi

# 直接编译目标程序restler_bin
if [[ -f "build-RestlerAuto.py" ]]; then
    echo "开始执行 build-RestlerAuto.py 脚本..."
    sudo python3 $PARENT_DIR/Build/build-RestlerAuto.py --repository_root_dir $PARENT_DIR/Build/restler-fuzzer/ --dest_dir $PARENT_DIR/restler_bin/
else
    echo "未找到 build-RestlerAuto.py 脚本文件"
fi

echo "安装和编译过程完成，如果需要删除本工具只需要删除dotnet即可"