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

# 複製構建的文件到 nginx 服務目錄
COPY --from=builder /app/build /usr/share/nginx/html

# 使用完整的 nginx.conf 覆蓋默認配置，避免 entrypoint 腳本干擾
COPY nginx.conf /etc/nginx/nginx.conf

# 暴露端口 8080
EXPOSE 8080

# 測試配置是否有效
RUN nginx -t

# 直接啟動 nginx
CMD ["nginx", "-g", "daemon off;"]
