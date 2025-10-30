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

# 安裝 envsubst（用於環境變量替換）
RUN apk add --no-cache gettext

# 複製 nginx 配置模板（包含環境變量佔位符）
COPY nginx.conf.template /etc/nginx/nginx.conf.template

# 複製 entrypoint 腳本（處理環境變量替換）
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 複製構建的文件到 nginx 服務目錄
COPY --from=builder /app/build /usr/share/nginx/html

# 使用 entrypoint 腳本啟動 nginx
ENTRYPOINT ["/entrypoint.sh"]
