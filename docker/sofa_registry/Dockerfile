# 使用基础镜像
FROM ubuntu:latest

# 设置工作目录
WORKDIR /app

# 安装 tree
RUN apt update && apt install -y tree openjdk-8-jdk

# 拷贝 registry-all.tgz 到镜像中
COPY registry-all.tgz .

RUN tar -zxvf registry-all.tgz

WORKDIR /app/registry-all

# COPY application.properties conf

RUN chmod +x -R bin

RUN tree ./bin

# 启动 registry-integration
CMD ["sh", "bin/integration/start.sh"]