from FuzzTargetBuild import *



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

    #工作路径配置
    FuzzTaskName = Fuzzconfigfile["fuzz_task_name"]
    ProjectID = Fuzzconfigfile["project_id"]
    CrrentFuzzWorkPath = Path(os.path.abspath(RESTLERFUZZ_ALLWORK_DIR)).joinpath(f"{FuzzTaskName}_{ProjectID}") # Fuzz工作目录

    APISpecFile = os.path.join(CrrentFuzzWorkPath, APISpec_Filename)
    CompileScriptFile = os.path.join(CrrentFuzzWorkPath, CompileScript_Filename)
    StartScriptFile = os.path.join(CrrentFuzzWorkPath, StartScript_Filename)



    # 存储这些信息工来工作使用
    Fuzz_config = {
        "package_filename": Package_Filename,
        "api_spec_name": APISpec_Filename,
        "compile_script_name": CompileScript_Filename,
        "start_script_name": StartScript_Filename,
        "fuzz_state_file": FuzzStateFile,
        "upload_package_file": UploadPackageFile,
        "api_spec_file": APISpecFile,
        "compile_script_file": CompileScriptFile,
        "start_script_file": StartScriptFile,
        "fuzz_work_path": CrrentFuzzWorkPath,
    }



    # 步骤0: 解压上传上来的目标文件
    try:
        # unzip_file(UploadPackageFile, None)
        update_fuzz_state(FuzzStateFile, "unzip_target_file", True)
    except Exception as e:
        ERR(f"解压目标文件{Package_Filename}失败: {e},整个Fuzz无法启动!运行终止")
        update_fuzz_state(FuzzStateFile, "unzip_target_file", False)
        return

    # 步骤1: 编译目标的OpenAPI文档
    try:
        compile_spec(Fuzz_config)
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
                        type=str, required=True, default=None)
    parser.add_argument('--uploadPath',
                        help='上传的压缩包文件路径',
                        type=str, required=True, default=None)
    parser.add_argument('--FuzzStateOutputPath',
                        help='希望Fuzz状态的输出路径',
                        type=str, required=True, default=None)
    parser.add_argument('--ALLFuzzWorkPath',
                        help='所有项目希望工作的目录',
                        type=str, required=False, default=None)
    args = parser.parse_args()

    # 使用 ALLFuzzWorkPath 参数
    if args.ALLFuzzWorkPath:
        RESTLERFUZZ_ALLWORK_DIR = args.ALLFuzzWorkPath
    
    #创建目标工作目录
    if not os.path.exists(RESTLERFUZZ_ALLWORK_DIR):
        os.makedirs(RESTLERFUZZ_ALLWORK_DIR)

    AutoFuzzMain(args.jsonfile,args.uploadPath,args.FuzzStateOutputPath)
