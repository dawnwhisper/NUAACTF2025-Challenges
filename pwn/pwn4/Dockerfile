# Dockerfile
FROM ubuntu:22.04

RUN sed -i 's|http://archive.ubuntu.com/ubuntu/|http://repo.huaweicloud.com/ubuntu/|g' /etc/apt/sources.list && \
    sed -i 's|http://security.ubuntu.com/ubuntu/|http://repo.huaweicloud.com/ubuntu/|g' /etc/apt/sources.list
RUN apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y lib32z1 xinetd && \
    apt-get install -y bc

WORKDIR /app

# 将当前目录下的所有文件复制到容器中
COPY . /app
RUN chmod 777 /app/httpd
RUN chmod 777 /app/cgi-bin/calc.cgi

# 默认 FLAG 环境变量，可在 docker run 时覆盖
ENV FLAG="default_flag"

# 暴露程序监听的端口（假设为 8080）
EXPOSE 8080

# 在启动容器时，将环境变量 FLAG 的内容写入 flag.txt, 然后启动 httpd 程序
CMD ["/bin/bash", "-c", "echo \"$FLAG\" > flag.txt && ./httpd"]