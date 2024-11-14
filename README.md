# RestlerFuzzer-Auto
restler-fuzzer的web fuzz工具,一键自动化fuzz!


# 如何编译项目
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"



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

