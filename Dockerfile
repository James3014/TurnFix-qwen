# 第一階段：構建 React 應用
FROM node:18-alpine AS builder

# 設置工作目錄
WORKDIR /app

# 複製 package 文件
COPY package.json ./

# 安裝依賴
RUN npm install

# 複製源代碼
COPY . .

# 構建 React 應用
RUN npm run build

# 第二階段：使用 nginx 服務構建的文件
FROM nginx:alpine

# 移除 nginx 默認配置，避免端口衝突
RUN rm /etc/nginx/conf.d/default.conf

# 複製 nginx 配置到 conf.d 目錄（nginx 會自動加載）
COPY nginx-simple.conf /etc/nginx/conf.d/default.conf

# 複製構建的文件到 nginx 服務目錄
COPY --from=builder /app/build /usr/share/nginx/html

# 暴露端口 8080
EXPOSE 8080

# 添加調試：顯示配置和啟動信息
RUN echo "==== Debugging Info ====" && \
    echo "nginx version:" && nginx -v && \
    echo "Config files:" && ls -la /etc/nginx/conf.d/

# 創建啟動腳本來輸出調試信息
RUN echo '#!/bin/sh' > /start.sh && \
    echo 'echo "=== Starting nginx ==="' >> /start.sh && \
    echo 'echo "Config file content:"' >> /start.sh && \
    echo 'cat /etc/nginx/conf.d/default.conf' >> /start.sh && \
    echo 'echo "Testing nginx config..."' >> /start.sh && \
    echo 'nginx -t' >> /start.sh && \
    echo 'echo "Starting nginx on port 8080..."' >> /start.sh && \
    echo 'exec nginx -g "daemon off;"' >> /start.sh && \
    chmod +x /start.sh

# 使用調試腳本啟動
CMD ["/start.sh"]
