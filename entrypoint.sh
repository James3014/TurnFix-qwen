#!/bin/sh
# 使用 envsubst 替换 nginx 配置中的环境变量
# 这解决了 nginx 无法直接读取 Bash 环境变量的问题

set -e

echo "Substituting environment variables in nginx.conf..."
# 使用 envsubst 替换配置文件中的 ${PORT:-80} 等变量
envsubst '${PORT}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

echo "Starting nginx..."
# 以前台模式启动 nginx，这样 Docker 容器不会退出
exec nginx -g 'daemon off;'
