from RunFuzzTool import *

def is_port_open(host, port):
    """ 检查指定端口是否开放 """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        sock.connect((host, port))
        return True
    except socket.error:
        return False
    finally:
        sock.close()

def stop_web_service(process):
    """ 停止 Web 服务 """
    INFO("准备停止 Web 服务...")
    process.terminate()  # 或者使用 process.kill()
    process.wait()
    INFO("Web 服务已停止!")

def handle_exit_signal(signal, frame, process):
    """ 捕获 SIGINT 信号时停止 Web 服务 """
    INFO("捕获到退出信号，准备停止 Web 服务...")
    stop_web_service(process)
    sys.exit(0)  # 退出程序

def cleanup(process):
    """ 在程序退出时清理 Web 服务进程 """
    INFO("程序结束，准备清理资源...")
    stop_web_service(process)

# 执行目标程序的脚本
def execute_script(Fuzz_Fileconfig):
    """ 执行指定的脚本
    Fuzz_Fileconfig["start_script_file"] : 脚本文件的绝对路径
    """
    INFO("开始执行脚本!")
    
    # 获取脚本文件的路径
    start_script_path = Fuzz_Fileconfig.get("start_script_file")
    
    if not start_script_path or not os.path.exists(start_script_path):
        ERR(f"脚本文件路径{start_script_path}不存在! 请检查配置.")
        raise ValueError("脚本文件路径不存在! 请检查配置.")

    DBG(f"执行脚本命令")
    with usedir(Fuzz_Fileconfig['fuzz_work_path']):
        command = f"bash \"{start_script_path}\""  # 假设我们使用bash来运行脚本
        print(f"command: {command}")
        # 非阻塞方式启动 Web 服务进程
        process = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)

        # 检查 Web 服务是否成功启动
        host = '127.0.0.1'  # 假设服务绑定到本地
        port = 2503  # 替换成实际的 Web 服务端口
        timeout = 30  # 超时时间，单位：秒
        start_time = time.time()

        while time.time() - start_time < timeout:
            if is_port_open(host, port):
                time.sleep(5)
                INFO(f"Web 服务在端口 {port} 启动成功!")
                break
            time.sleep(1)
        else:
            ERR("Web 服务启动失败!")
            process.terminate()
            raise RuntimeError("Web 服务启动失败!")
        
        return process  # 返回进程对象供后续使用