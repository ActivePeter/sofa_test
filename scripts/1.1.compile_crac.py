# CRAC can't be compiled in container because it uses vfork



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

    
def compile_crac():
    os_system_sure("apt install build-essential autoconf -y")
    os.system("git clone https://github.com/openjdk/crac.git")
    os.chdir("crac")
    os_system_sure("git checkout crac-17+6")
    installs=[
        'libfontconfig1-dev',
        'libx11-dev libxrender-dev libxrandr-dev libxtst-dev libxt-dev',
        'zip unzip',
        'file',
        'build-essential',
        'libasound2-dev',
        'libcups2-dev'
    ]
    os_system_sure("apt update")
    os_system_sure("apt install {} -y".format(" ".join(installs)))
    os_system_sure("bash configure")
    os_system_sure("make images")
    # os_system_sure("mv build/linux-x86_64-server-release/images/jdk/ .")

compile_crac()