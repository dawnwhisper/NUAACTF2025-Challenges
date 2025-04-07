FROM nginx:alpine

# 设置工作目录
WORKDIR /usr/share/nginx/html

# 复制前端代码到容器
COPY ./html /usr/share/nginx/html

# 设置正确的权限（可选，确保 Nginx 能正确读取文件）
RUN chmod -R 755 /usr/share/nginx/html

# 暴露端口
EXPOSE 90

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]
