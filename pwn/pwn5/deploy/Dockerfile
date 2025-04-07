FROM ubuntu:22.04

# 更新源并安装必要工具
RUN sed -i 's|http://archive.ubuntu.com/ubuntu/|http://repo.huaweicloud.com/ubuntu/|g' /etc/apt/sources.list && \
    sed -i 's|http://security.ubuntu.com/ubuntu/|http://repo.huaweicloud.com/ubuntu/|g' /etc/apt/sources.list

RUN apt-get update && apt-get install -y \
    xinetd \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录为 /home/ctf
WORKDIR /home/ctf

# 拷贝服务程序（例如 attachment）
COPY ./src/attachment ./attachment
# 设置服务程序为可执行
RUN chmod +x /home/ctf/attachment

# 创建普通用户 user（该用户用于运行服务程序）
RUN useradd -ms /bin/sh user

# 直接对 /usr/bin/base64 赋予 suid 权限
RUN chown root:root /usr/bin/base64 && \
    chmod 4755 /usr/bin/base64

# 拷贝 xinetd 配置文件到 /etc/xinetd.d/ctf
COPY ./config/ctf.xinetd /etc/xinetd.d/ctf
RUN echo "Blocked by ctf_xinetd" > /etc/banner_fail

# 拷贝 entrypoint 脚本到容器根目录并赋予执行权限
COPY ./service/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# 暴露 9999 端口
EXPOSE 9999

# 以 entrypoint 脚本启动
ENTRYPOINT ["/docker-entrypoint.sh"]