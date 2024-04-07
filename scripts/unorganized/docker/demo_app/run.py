import os
import docker

CUR_FPATH = os.path.abspath(__file__)
CUR_FDIR = os.path.dirname(CUR_FPATH)
DATABASE_HOST = "192.168.31.87"
DATABASE_PW = "mysqltest"


# chdir to the directory of this script
os.chdir(CUR_FDIR)

# 构建 Docker 镜像
def build_image():
    # copy ../../kc-sofastack-demo to ./kc-sofastack-demo
    os.system("rm -rf ./kc-sofastack-demo")
    os.system("cp -r ../../kc-sofastack-demo ./kc-sofastack-demo")

    # load kc-sofastack-demo/DDL.sql to database
    os.system(f"mysql -h{DATABASE_HOST} -uroot -p{DATABASE_PW} < ./kc-sofastack-demo/DDL.sql")

    os.system("cp /usr/bin/tree ./")
    os.system("docker build -t sofa_demo_app . --no-cache")

# 运行 Docker 容器
def run_container():
    os.system("docker-compose down")
    os.system("docker-compose up -d")

    # print("Docker 容器已启动")

def ls_images():
    client = docker.from_env()
    images = client.images.list()
    for image in images:
        print(image.tags)



if __name__ == "__main__":
    # 构建 Docker 镜像
    build_image()

    # # 查看 Docker 镜像
    # ls_images()

    # # # 运行 Docker 容器
    run_container()
