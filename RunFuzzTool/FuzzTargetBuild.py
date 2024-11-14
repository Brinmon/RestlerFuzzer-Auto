import argparse
import contextlib
import os
import subprocess
import json
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


#编译swagger或openapi文件
def compile_spec(fuzz_config):
    """ 编译指定的 API 规范

    @param api_spec_path: 要编译的 Swagger 文件的绝对路径
    @type  api_spec_path: 字符串
    @param restler_dll_path: RESTler 驱动程序 DLL 的绝对路径
    @type  restler_dll_path: 字符串

    @return: None
    @rtype : None

    """
    DBG(f"开始编译OpenAPI文档: {fuzz_config['api_spec_name']}")
    # 读取环境中Restler的相关环境变量
    # 检查环境变量是否存在
    restlerbin_root = os.environ.get('RESTLERBIN_ROOT')
    if restlerbin_root is None:
        restlerbin_root = '/usr/local/bin/restler_bin'
    restler_dll_path = Path(restlerbin_root).joinpath('restler','Restler.dll')   # 获取环境变量中的根路径并添加restler_bin
    DBG(f"找到的Dll路径为: {restler_dll_path}")
    if not restler_dll_path.exists():  # 检查构建的DLL路径是否存在
        ERR(f"Restler DLL路径{restler_dll_path}不存在!请检查环境是否配置正确!")  # 如果不存，打印错误信息
        raise ValueError("Restler DLL路径不存在!请检查环境变量配置异常!")
    
    #创建目标工作目录
    if not os.path.exists(fuzz_config['fuzz_work_path']):
        os.makedirs(fuzz_config['fuzz_work_path'])

    DBG(f"执行编译编译命令")
    with usedir(fuzz_config['fuzz_work_path']):
        command=f"dotnet \"{restler_dll_path}\" compile --api_spec \"{fuzz_config['api_spec_file']}\""
        print(f"command: {command}")
        subprocess.run(command, shell=True)
        DBG(f"执行完毕!")

# 编译目标程序
def compile_target(config, working_dir):
    pass

#执行目标程序的脚本
def execute_script(script_name, working_dir):
    pass

def unzip_file(zip_path, extract_to):
    pass