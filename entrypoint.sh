#!/bin/sh
# 使用 envsubst 替换 nginx 配置中的环境变量
# 这解决了 nginx 无法直接读取 Bash 环境变量的问题

set -e

# 如果 PORT 环境变量没有设置，则设置默认值
if [ -z "$PORT" ]; then
    export PORT=80
    echo "PORT not set, using default port 80"
else
    echo "Using PORT=$PORT from environment"
fi

echo "Substituting environment variables in nginx.conf..."
# 使用 envsubst 替换配置文件中的 ${PORT} 变量
envsubst '${PORT}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

echo "nginx.conf configuration:"
cat /etc/nginx/nginx.conf | grep "listen" || true

echo "Starting nginx..."
# 以前台模式启动 nginx，这样 Docker 容器不会退出
exec nginx -g 'daemon off;'
