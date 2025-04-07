#!/bin/bash
# 如果注入了 FLAG 环境变量，则生成 /flag 文件并设置为 root 所有
if [ -n "$FLAG" ]; then
    echo "$FLAG" > /home/ctf/flag
    chown root:root /home/ctf/flag
    chmod 400 /home/ctf/flag
    unset FLAG
fi

echo "Starting xinetd..."
# 启动 xinetd 服务，保持前台运行（-dontfork）
exec /usr/sbin/xinetd -dontfork