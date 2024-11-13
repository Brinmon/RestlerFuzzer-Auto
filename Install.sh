#!/bin/bash

# 获取当前目录
current_dir=$PWD

# 检查是否已设置环境变量 RESTLERFUZZERAUTO_ROOT
if [ -z "$RESTLERFUZZERAUTO_ROOT" ]; then
    echo "未检测到环境变量 RESTLERFUZZERAUTO_ROOT，使用当前目录 ($current_dir) 作为默认值。"
    export RESTLERFUZZERAUTO_ROOT=$current_dir
    # 永久化环境变量 RESTLERFUZZERAUTO_ROOT
    echo "正在设置环境变量 RESTLERFUZZERAUTO_ROOT..."
    echo "export RESTLERFUZZERAUTO_ROOT=$current_dir" >> $HOME/.bashrc
    source $HOME/.bashrc
    echo "已将 RESTLERFUZZERAUTO_ROOT 环境变量持久化，路径为 $RESTLERFUZZERAUTO_ROOT"
else
    echo "当前环境变量 RESTLERFUZZERAUTO_ROOT 已设置为 $RESTLERFUZZERAUTO_ROOT"
    # 检查当前目录与已设置的环境变量是否一致
    if [ "$RESTLERFUZZERAUTO_ROOT" != "$current_dir" ]; then
        echo "当前目录 ($current_dir) 与已设置的 RESTLERFUZZERAUTO_ROOT ($RESTLERFUZZERAUTO_ROOT) 不一致。"
        read -p "是否更新环境变量 RESTLERFUZZERAUTO_ROOT 为当前目录？(y/n): " choice
        if [ "$choice" == "y" ]; then
            export RESTLERFUZZERAUTO_ROOT=$current_dir
            # 更新并永久化环境变量
            echo "正在更新并设置环境变量 RESTLERFUZZERAUTO_ROOT..."
            echo "export RESTLERFUZZERAUTO_ROOT=$current_dir" >> $HOME/.bashrc
            source $HOME/.bashrc
            echo "已将 RESTLERFUZZERAUTO_ROOT 环境变量持久化，路径为 $RESTLERFUZZERAUTO_ROOT"
        else
            echo "未更新环境变量。"
        fi
    fi
fi

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
    echo "未检测到 .NET 环境，正在下载并安装 .NET 6.0 SDK..."
    # 下载并安装 .NET 6.0 SDK
    wget https://download.visualstudio.microsoft.com/download/pr/12ee34e8-640c-400e-a6dc-4892b442df92/81d40fc98a5bbbfbafa4cc1ab86d6288/dotnet-sdk-6.0.427-linux-x64.tar.gz
    mkdir -p $HOME/dotnet
    tar -zxf dotnet-sdk-6.0.100-linux-x64.tar.gz -C $HOME/dotnet

    # 设置 DOTNET_ROOT 和 PATH
    echo "安装完成，正在设置环境变量..."
    export PATH=$PATH:$DOTNET_ROOT
    export PATH=$PATH:$DOTNET_ROOT
    # 将 DOTNET_ROOT 和 PATH 持久化到 ~/.bashrc (或 ~/.zshrc, 视你的 shell 配置文件而定)
    echo 'export DOTNET_ROOT=$HOME/dotnet' >> $HOME/.bashrc
    echo 'export PATH=$PATH:$DOTNET_ROOT' >> $HOME/.bashrc

    # 使配置立即生效
    source $HOME/.bashrc

    echo "已将 DOTNET_ROOT 和 PATH 环境变量持久化，并已设置为 $HOME/dotnet"
fi

# 检查 Python 环境
if command -v python3 &>/dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "Python 环境已安装：$PYTHON_VERSION ,推荐版本 Python 3.8.2 "
else
    echo "未检测到 Python 环境，正在安装 Python 3.8..."
    sudo apt-get update
    sudo apt-get install python3.8 python3.8-venv python3.8-dev
    echo "Python 3.8 安装完成"
fi




# 检查目标项目目录是否已存在
if [ -d "$RESTLERFUZZERAUTO_ROOT/restler-fuzzer" ]; then
    echo "restler-fuzzer 项目已存在，跳过克隆步骤..."
else
    # 克隆目标项目
    echo "正在克隆 restler-fuzzer 项目..."
    git clone https://github.com/microsoft/restler-fuzzer.git
fi

# 检查是否已编译过，检测是否存在 restler_bin 目录
if [ -d "$RESTLERFUZZERAUTO_ROOT/restler_bin" ]; then
    echo "restler_bin 目录已存在，跳过编译步骤，编译完毕。"
else
    if [[ -f "build-RestlerAuto.py" ]]; then
        echo "开始执行 build-RestlerAuto.py 脚本..."
        python3 ./build-RestlerAuto.py --repository_root_dir $RESTLERFUZZERAUTO_ROOT/restler-fuzzer --dest_dir ./restler_bin/
    else
        echo "未找到 build-RestlerAuto.py 脚本文件"
    fi
fi

echo "安装和编译过程完成,需要重新启动一个新的会话环境变量才会生效!"
