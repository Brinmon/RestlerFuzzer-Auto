from RunFuzzTool import *

#编译swagger或openapi文件
def compile_spec(Fuzz_Fileconfig):
    """ 编译指定的 API 规范
    使用的参数有:
    Fuzz_Fileconfig['fuzz_work_path'] : 工作目录
    Fuzz_Fileconfig['api_spec_name'] : API 规范文件名
    Fuzz_Fileconfig['api_spec_file'] : API 规范文件绝对路径
    """
    
    # 获取当前文件的绝对路径
    current_file_path = os.path.abspath(__file__)
    # 获取当前文件所在的目录
    current_directory = os.path.dirname(current_file_path)
    parent_directory = os.path.dirname(current_directory) 
    INFO(f"开始编译OpenAPI文档: {Fuzz_Fileconfig['api_spec_name']}")

    restler_dll_path = Path(parent_directory).joinpath('restler_bin','restler','Restler.dll')   
    DBG(f"找到的Dll路径为: {restler_dll_path}")
    if not restler_dll_path.exists():  # 检查构建的DLL路径是否存在
        ERR(f"Restler DLL路径{restler_dll_path}不存在!请检查环境是否配置正确!")  # 如果不存，打印错误信息
        raise ValueError("Restler DLL路径不存在!请检查环境变量配置异常!")
    
    #创建目标工作目录
    if not os.path.exists(Fuzz_Fileconfig['fuzz_work_path']):
        os.makedirs(Fuzz_Fileconfig['fuzz_work_path'])

    DBG(f"执行编译编译命令")
    with usedir(Fuzz_Fileconfig['fuzz_work_path']):
        command=f"dotnet \"{restler_dll_path}\" compile --api_spec \"{Fuzz_Fileconfig['api_spec_file']}\""
        print(f"command: {command}")
        subprocess.run(command, shell=True)
        INFO(f"API 文档编译执行完毕!")

# 编译目标程序
def compile_target(Fuzz_Fileconfig):
    """ 编译指定的目标程序
    Fuzz_Fileconfig["compile_script_file"] : 编译脚本文件的绝对路径
    """
    INFO("开始编译目标程序!")
    # 获取编译脚本的路径
    compile_script_path = Fuzz_Fileconfig.get("compile_script_file")
    
    if not compile_script_path or not os.path.exists(compile_script_path):
        ERR(f"编译脚本路径{compile_script_path}不存在! 请检查配置.")
        raise ValueError("编译脚本路径不存在! 请检查配置.")

    # 创建目标工作目录
    if not os.path.exists(Fuzz_Fileconfig['fuzz_work_path']):
        os.makedirs(Fuzz_Fileconfig['fuzz_work_path'])

    DBG(f"执行编译命令")
    with usedir(Fuzz_Fileconfig['fuzz_work_path']):
        command = f"bash \"{compile_script_path}\""  # 假设我们使用bash来运行编译脚本
        print(f"command: {command}")
        result = subprocess.run(command, shell=True)

        if result.returncode != 0:
            ERR("目标程序编译失败!")
            raise RuntimeError("目标程序编译失败!")
        
        INFO("目标程序编译成功!")

#解压目标程序
def unzip_file(Fuzz_Fileconfig):
    """
    使用的参数有:
    Fuzz_Fileconfig['upload_package_file']  : 上传的压缩包文件的绝对路径
    Fuzz_Fileconfig['fuzz_work_path'] : 解压到本次任务的工作路径
    """
    package_file = Fuzz_Fileconfig['upload_package_file']
    fuzz_work_path = Fuzz_Fileconfig['fuzz_work_path']
    
    INFO(f"开始解压上传上来的文件: {package_file}")
    
    # 确保工作目录存在
    os.makedirs(fuzz_work_path, exist_ok=True)

    # 根据文件扩展名判断解压方式
    if package_file.endswith('.zip'):
        with zipfile.ZipFile(package_file, 'r') as zip_ref:
            zip_ref.extractall(fuzz_work_path)
            INFO(f"已解压缩 ZIP 文件到: {fuzz_work_path}")
            
    elif package_file.endswith(('.tar', '.tar.gz', '.tar.bz2')):
        with tarfile.open(package_file, 'r:*') as tar_ref:
            tar_ref.extractall(fuzz_work_path)
            INFO(f"已解压缩 TAR 文件到: {fuzz_work_path}")
    
    else:
        ERR(f"不支持的文件格式: {package_file}")
        raise ValueError(f"不支持的文件格式: {package_file}")