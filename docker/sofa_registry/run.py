import os
import docker
import requests
import time

CUR_FPATH = os.path.abspath(__file__)
CUR_FDIR = os.path.dirname(CUR_FPATH)

# chdir to the directory of this script
os.chdir(CUR_FDIR)

HOST_IP = "192.168.232.129"

# 下载
# https://github.com/sofastack/sofa-registry/releases/download/v6.1.9/registry-all.tgz
def download():
    # check if the file exists
    if os.path.exists("registry-all.tgz"):
        print("registry-all.tgz 文件已存在")
        return
    os.system("wget https://github.com/sofastack/sofa-registry/releases/download/v6.1.9/registry-all.tgz")

def unzip():
    if not os.path.exists("registry-all.tgz"):
        print("registry-all.tgz 文件不存在")
        return
    if os.path.exists("registry-all"):
        print("registry-all 文件夹已存在")
        return
    os.system("tar -zxvf registry-all.tgz")

# 构建 Docker 镜像
def build_image():
    os.system("docker build -t sofa_registry .")

# 运行 Docker 容器
def run_container():
    os.system("docker-compose down")
    os.system("docker-compose up -d")

def checks():
    #test sofa registry
    time.sleep(5)
    # 200 curl http://localhost:9615/health/check
    # 200 curl http://localhost:9622/health/check
    # 200 curl http://localhost:9603/health/check
    def check(path):
        res=requests.get(path)
        print(res.status_code)
        if res.status_code==200:
            print("success")
        else:
            print("fail")
    check(f"http://{HOST_IP}:9615/health/check")
    check(f"http://{HOST_IP}:9622/health/check")
    check(f"http://{HOST_IP}:9603/health/check")


def ls_images():
    client = docker.from_env()
    images = client.images.list()
    for image in images:
        print(image.tags)



if __name__ == "__main__":
    # 创建数据库
    os.system(f'echo "create database registrymetadb " | mysql -h {HOST_IP} -u root -pmysqltest')
    os.system(f'mysql -h {HOST_IP} -u root -pmysqltest registrymetadb < create_table.sql')
    
    # use python
    
    
    # 下载镜像
    download()

    # 解压镜像
    unzip()

    # 构建 Docker 镜像
    build_image()

    # 查看 Docker 镜像
    ls_images()

    # # 运行 Docker 容器
    run_container()

    checks()