# RestlerFuzzer-Auto
restler-fuzzer的web fuzz工具,一键自动化fuzz!


# 如何编译项目
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"

## python依赖
```d
ub20@ub20:~/RestlerFuzzer-Auto/ExampleInput$ pip install psutil
```


# 编译API描述文件,支持yml和json格式的文档
```d
ub20@ub20:~/RestlerFuzzer-Auto$ sudo python ./RunFuzzTool/RestlerFuzzStart.py --jsonfile ./ExampleInput/Fuzz.json --uploadPath ./TestDir/ --FuzzStateOutputPath ./TestDir/ --ALLFuzzWorkPath ./TestDir/
DEBUG: 开始编译OpenAPI文档: open_api_3.yaml
DEBUG: 找到的Dll路径为: /usr/local/bin/restler_bin/restler/Restler.dll
DEBUG: 执行编译编译命令
command: dotnet "/usr/local/bin/restler_bin/restler/Restler.dll" compile --api_spec "/home/ub20/RestlerFuzzer-Auto/TestDir/example_fuzz_task_1/open_api_3.yaml"
Starting task Compile...
Task Compile succeeded.
Collecting logs...
DEBUG: 执行完毕!
```

# Examples
```d
ub20@ub20:~/RestlerFuzzer-Auto/ExampleInput$ ls
build.sh  Fuzz.json  open_api_3.yaml  qri  start.sh

```

# 运行RestlerFuzzer-Auto
简单的案例运行:
```d
 python3 ./RestlerFuzzStart.py --jsonfile ./ExampleInput/Fuzz.json 
```






# 开发日志
## 2024-11-14
```d
DevelopmentLog:
成功验证:
subprocess.Popen开启一个进程有pid
直接杀死这个pid,无法完全杀死这个进程的子进程
这个进程启动了一个shell脚本,shell脚本又启动了一个web服务
所以在这个subprocess.Popen进程中存在两个子进程即使杀死了subprocess.Popen,其他的两个子进程也不会停止!
所以需要先终止子进程在杀死父进程
INFO: Web 服务在端口 2503 启动成功!
16041
INFO: 开始启动Fuzz程序...
INFO: 开始输出Fuzz测试结果...
INFO: 程序结束，准备清理资源...
INFO: 准备停止 Web 服务...
终止子进程 16042
终止子进程 16044
INFO: Web 服务及其所有子进程已停止!
ub20@ub20:~/RestlerFuzzer-Auto$ ps aux | grep qri
ub20       16044  5.4  1.4 4942428 56388 ?       Sl   16:14   0:01 ./qri connect --setup --migrate --no-prompt
ub20       16161  0.0  0.0  12000   720 pts/3    S+   16:15   0:00 grep --color=auto qri
ub20@ub20:~/RestlerFuzzer-Auto$ ps -p 16042 -o pid,ppid,user,%cpu,%mem,command
    PID    PPID USER     %CPU %MEM COMMAND
  16042       1 ub20      0.0  0.0 bash /home/ub20/RestlerFuzzer-Auto/TestDir/example_fuzz_task_1/start.sh
```

