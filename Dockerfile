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

# 移除 nginx 默認配置
RUN rm /etc/nginx/conf.d/default.conf

# 複製我們的 nginx 配置
COPY nginx-simple.conf /etc/nginx/conf.d/default.conf

# 創建健康檢查文件
RUN echo "OK" > /usr/share/nginx/html/health

# 暴露端口 8080
EXPOSE 8080

# 測試配置是否有效
RUN nginx -t

# 直接啟動 nginx（不使用自定義腳本）
CMD ["nginx", "-g", "daemon off;"]
