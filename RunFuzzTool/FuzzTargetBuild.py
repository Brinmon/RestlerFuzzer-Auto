import contextlib
import os
import subprocess

import zipfile
import tarfile
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
    使用的参数有:
    fuzz_config['fuzz_work_path']
    fuzz_config['api_spec_name']
    fuzz_config['api_spec_file']
    """
    
    # 获取当前文件的绝对路径
    current_file_path = os.path.abspath(__file__)
    # 获取当前文件所在的目录
    current_directory = os.path.dirname(current_file_path)
    DBG(f"开始编译OpenAPI文档: {fuzz_config['api_spec_name']}")

    restler_dll_path = Path(current_directory).joinpath('restler_bin','restler','Restler.dll')   
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

def unzip_file(fuzz_config):
    """编译指定的 API 规范
    使用的参数有:
    fuzz_config['package_filename']
    fuzz_config['fuzz_work_path']
    """
    package_filename = fuzz_config['package_filename']
    fuzz_work_path = fuzz_config['fuzz_work_path']
    
    DBG(f"开始解压上传上来的文件: {package_filename}")
    
    # 确保工作目录存在
    os.makedirs(fuzz_work_path, exist_ok=True)

    # 根据文件扩展名判断解压方式
    if package_filename.endswith('.zip'):
        with zipfile.ZipFile(package_filename, 'r') as zip_ref:
            zip_ref.extractall(fuzz_work_path)
            DBG(f"已解压缩 ZIP 文件到: {fuzz_work_path}")
            
    elif package_filename.endswith(('.tar', '.tar.gz', '.tar.bz2')):
        with tarfile.open(package_filename, 'r:*') as tar_ref:
            tar_ref.extractall(fuzz_work_path)
            DBG(f"已解压缩 TAR 文件到: {fuzz_work_path}")
    
    else:
        DBG(f"不支持的文件格式: {package_filename}")