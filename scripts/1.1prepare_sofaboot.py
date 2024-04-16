
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


# env java home  openjdk 17
os.environ['JAVA_HOME'] = "/usr/lib/jvm/java-17-openjdk-amd64"
os.system("git clone https://github.com/340Lab/sofa-boot")
os.chdir("sofa-boot")
os_system_sure("git checkout 3.1.4crac")
os_system_sure("mvn clean install -DskipTests -Dmaven.javadoc.skip=true")