import contextlib
import os
import subprocess
import time
import zipfile
import tarfile
import sys
import socket
import signal
import atexit
from pathlib import Path

#路径常量
RESTLERFUZZ_ALLWORK_DIR = '/restler_work_dir'

# 全局调试标志
debug_mode = True
info_mode = True

# 设置输出模式
def set_print_mode(info_enabled, debug_enabled):
    """设置输出模式"""
    global info_mode, debug_mode
    info_mode = info_enabled
    debug_mode = debug_enabled
   
def DBG(message):
    """输出调试信息 (蓝色)"""
    if debug_mode:
        print(f"\033[94mDEBUG: {message}\033[0m")  # ANSI 转义序列，\033[94m 是蓝色，\033[0m 重置为默认颜色

def ERR(message):
    """输出错误信息 (红色)"""
    print(f"\033[91mERROR: {message}\033[0m")  # ANSI 转义序列，\033[91m 是红色，\033[0m 重置为默认颜色

def INFO(message):
    """输出信息 (绿色)"""
    if info_mode:
        print(f"\033[92mINFO: {message}\033[0m")  # ANSI 转义序列，\033[92m 是绿色，\033[0m 重置为默认颜色


@contextlib.contextmanager
def usedir(dir):
    """ 一个帮助器，适用于 'with' 语句，用于将当前目录更改为
    @dir，且在 'with' 结束后将目录更改回原始目录。

    可以被视为 pushd，'with' 范围结束后自动执行 popd
    """
    curr = os.getcwd()  # 获取当前工作目录
    os.chdir(dir)  # 切换到指定的目录
    try:
        yield  # 生成器，可以在 with 块内执行代码
    finally:
        os.chdir(curr)  # 确保在结束时切换回原来的目录