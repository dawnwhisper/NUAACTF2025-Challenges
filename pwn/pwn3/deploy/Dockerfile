FROM ubuntu:22.04

# 制作者信息
LABEL auther_template="CTF-Archives"

RUN sed -i 's|http://archive.ubuntu.com/ubuntu/|http://repo.huaweicloud.com/ubuntu/|g' /etc/apt/sources.list && \
    sed -i 's|http://security.ubuntu.com/ubuntu/|http://repo.huaweicloud.com/ubuntu/|g' /etc/apt/sources.list
RUN apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y lib32z1 xinetd libasan6

# 新建用户，并进行账户改变
RUN useradd -m ctf
WORKDIR /home/ctf

# 复制相关lib，并处理环境
RUN cp -R /usr/lib* /home/ctf

# 配置特殊管道映射
RUN mkdir /home/ctf/dev && \
    mknod /home/ctf/dev/null c 1 3 && \
    mknod /home/ctf/dev/zero c 1 5 && \
    mknod /home/ctf/dev/random c 1 8 && \
    mknod /home/ctf/dev/urandom c 1 9 && \
    chmod 666 /home/ctf/dev/*

# 设置xinetd启动之后，chroot限制能使用的bin程序
RUN mkdir /home/ctf/bin && \
    cp /bin/sh /home/ctf/bin && \
    cp /bin/ls /home/ctf/bin && \
    cp /bin/cat /home/ctf/bin && \
    cp /usr/bin/timeout /home/ctf/bin

# 部署xinetd服务
COPY ./config/ctf.xinetd /etc/xinetd.d/ctf
RUN echo "Blocked by ctf_xinetd" > /etc/banner_fail

# 复制容器启动脚本
COPY ./service/docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

# 部署程序
COPY ./src/attachment /home/ctf/attachment
COPY ./src/runner /home/ctf/runner

# 初始化flag
RUN chown -R root:ctf /home/ctf && \
    chmod -R 750 /home/ctf && \
    touch /home/ctf/flag && \
    chmod 744 /home/ctf/flag

EXPOSE 9999

# 指定容器入口点
ENTRYPOINT ["/bin/bash","/docker-entrypoint.sh"]
