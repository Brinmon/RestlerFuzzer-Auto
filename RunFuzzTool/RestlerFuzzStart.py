from FuzzTargetBuild import *

#路径常量
RESTLERFUZZ_TEMP_DIR = '/restler_work_dir'

# 全局调试标志
debug_mode = False
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

#读取json文件
def read_config(file_path):
    """读取JSON配置文件并返回内容"""
    with open(file_path, 'r') as f:
        return json.load(f)

#更新fuzz状态
def update_fuzz_state(state_file, step_name, success):
    """更新FuzzState.json中的步骤执行状态"""
    # 读取当前状态文件内容
    try:
        with open(state_file, 'r') as f:
            state_data = json.load(f)
    except FileNotFoundError:
        # 如果文件不存在，则初始化状态数据
        state_data = {}
    except json.JSONDecodeError:
        print(f"读取状态文件失败，JSON格式错误: {state_file}")
        return

    # 更新步骤执行状态
    state_data[step_name] = success

    # 将更新后的状态写回文件
    with open(state_file, 'w') as f:
        json.dump(state_data, f, ensure_ascii=False, indent=4)

def AutoFuzzMain(jsonfile,UploadPath,FuzzStateFilePath):
    #检测参数是否完整
    if jsonfile is None or UploadPath is None or FuzzStateFilePath is None:
        ERR("参数不完整，请检查!")
        return

    # 读取json文件
    Fuzzconfigfile = read_config(jsonfile)

    #获取json文件中的相关信息
    Package_Filename = Fuzzconfigfile["package_filename"]
    APISpec_Filename = Fuzzconfigfile["api_spec_name"]
    CompileScript_Filename = Fuzzconfigfile["compile_script_name"]
    StartScript_Filename = Fuzzconfigfile["start_script_name"]

    # 路径配置
    FuzzStateFile = os.path.join(FuzzStateFilePath, "FuzzState.json")
    UploadPackageFile = os.path.join(UploadPath, Package_Filename)
    APISpecFile = os.path.join(UploadPath, APISpec_Filename)
    CompileScriptFile = os.path.join(UploadPath, CompileScript_Filename)
    StartScriptFile = os.path.join(UploadPath, StartScript_Filename)

    FuzzWorkPath = os.path.join(UploadPath, StartScript_Filename)  # Fuzz工作目录

    # 读取环境中Restler的相关环境变量
    restler_dll_path = Path(os.environ.get('RESTLERFUZZERAUTO_ROOT')+'/restler_bin')   # 获取环境变量中的根路径并添加restler_bin
    if not restler_dll_path.exists():  # 检查构建的DLL路径是否存在
        ERR(f"Restler DLL路径{restler_dll_path}不存在!请检查环境变量是否配置正确!")  # 如果不存，打印错误信息
        return  # 退出当前函数

    # 步骤0: 解压上传上来的目标文件
    try:
        unzip_file(UploadPackageFile, None)
        update_fuzz_state(FuzzStateFile, "unzip_target_file", True)
    except Exception as e:
        ERR(f"解压目标文件{Package_Filename}失败: {e},整个Fuzz无法启动!运行终止")
        update_fuzz_state(FuzzStateFile, "unzip_target_file", False)
        return

    # 步骤1: 编译目标的OpenAPI文档
    try:
        compile_spec(APISpecFile, restler_dll_path.absolute())
        update_fuzz_state(FuzzStateFile, "compile_openapi_document", True)
    except Exception as e:
        print(f"编译OpenAPI文档失败: {e},整个Fuzz无法启动!运行终止")
        update_fuzz_state(FuzzStateFile, "compile_openapi_document", False)
        return

    # 步骤2: 执行Build.sh编译目标程序
    try:
        # compile_target(config)
        update_fuzz_state(FuzzStateFile, "execute_build_script", True)
    except Exception as e:
        ERR(f"执行{CompileScriptFile}失败: {e},可能存在问题!")
        update_fuzz_state(FuzzStateFile, "execute_build_script", False)

    # 步骤3: 执行Start.sh启动目标程序
    try:
        # execute_script(config)
        update_fuzz_state(FuzzStateFile, "execute_start_script", True)
    except Exception as e:
        ERR(f"执行{StartScriptFile}失败: {e},可能存在问题!")
        update_fuzz_state(FuzzStateFile, "execute_start_script", False)

    # 步骤4: 启动Fuzz程序
    try:
        # start_fuzzing(config)
        update_fuzz_state(FuzzStateFile, "start_fuzzing", True)
    except Exception as e:
        ERR(f"启动Fuzz程序失败: {e},存在重大问题!请重新审查!")
        update_fuzz_state(FuzzStateFile, "start_fuzzing", False)
        return

    # 步骤5: 输出Fuzz测试结果
    try:
        # output_fuzzing_results(config)
        update_fuzz_state(FuzzStateFile, "output_fuzzing_results", True)
    except Exception as e:
        ERR(f"输出Fuzz测试结果失败: {e},存在重大问题!请重新审查!")
        update_fuzz_state(FuzzStateFile, "output_fuzzing_results", False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--jsonfile',
                        help='读取json文件',
                        type=str, required=False, default=None)
    parser.add_argument('--uploadPath',
                        help='上传的压缩包文件路径',
                        type=str, required=False, default=None)
    parser.add_argument('--FuzzStatePath',
                        help='希望Fuzz状态的输出路径',
                        type=str, required=False, default=None)
    parser.add_argument('--FuzzWorkPath',
                        help='希望Fuzz状态的输出路径',
                        type=str, required=False, default=None)
    args = parser.parse_args()
    AutoFuzzMain(args.jsonfile,args.uploadPath,args.FuzzStatePath)