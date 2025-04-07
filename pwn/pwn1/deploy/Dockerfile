FROM python:3.9-slim

WORKDIR /app

# # 替换apt源为华为云源，并更新软件包索引
# RUN sed -i 's|http://deb.debian.org|http://repo.huaweicloud.com|g' /etc/apt/sources.list && \
#     sed -i 's|http://security.debian.org|http://repo.huaweicloud.com|g' /etc/apt/sources.list && \
#     apt-get update

# 将当前目录下的所有文件复制到容器中
COPY . /app

EXPOSE 12345

# 在启动时，从FLAG环境变量写入flag.txt，然后运行程序
CMD ["/bin/sh", "-c", "echo \"$FLAG\" > flag.txt && python src.py"]