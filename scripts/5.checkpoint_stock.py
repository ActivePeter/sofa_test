
### chdir
import os
CUR_FPATH = os.path.abspath(__file__)
CUR_FDIR = os.path.dirname(CUR_FPATH)
# chdir to the directory of this script
os.chdir(CUR_FDIR)



### utils
def os_system_sure(command):
    print(f"执行命令：{command}")
    result = os.system(command)
    if result != 0:
        print(f"命令执行失败：{command}")
        exit(1)
    print(f"命令执行成功：{command}")



JAR_PATH="../kc-sofastack-demo/stock-mng/target/stock-mng-0.0.1-SNAPSHOT.jar"



os.system(f"jcmd {JAR_PATH} JDK.checkpoint")




import subprocess
import re
import psutil

# def get_fd_info(pid):
#     try:
#         # 执行 ls -l /proc/[PID]/fd 命令并获取输出
#         result = subprocess.run(['ls', '-l', '/proc/{}/fd'.format(pid)], capture_output=True, text=True, check=True)
#         # 输出结果
#         return result.stdout
#     except subprocess.CalledProcessError as e:
#         # 如果命令执行失败，打印错误信息
#         print("Error:", e.stderr)
# 调用函数并传入进程的 PID


# PID=11747
# process=psutil.Process(PID)
# open_files = process.open_files()
# for file_info in open_files:
#     print(file_info)
#     try:
#         # file_info.fd.close()

#         os_system_sure("kill -9 {} {}",PID,file_info.fd)
#     except Exception as e:
#         print('failed toclose pid {} fd {}',e)


# opened_fds=get_fd_info(PID)
# for line in opened_fds.split("\n"):
#     if line.find(CUR_FDIR)!=-1:
#         def extract_fd(line):
#             pattern = r"(\d+)\s*->"  # 匹配箭头之前的数字部分
#             match = re.search(pattern, line)
#             if match:
#                 return match.group(1)
#             return None

#         fd=extract_fd(line)
#         print("line:",line)
#         print("fd:",fd)
