/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export', // 將 Next.js 應用導出為靜態網站
  trailingSlash: true, // 在所有路徑後添加斜杠
  images: {
    unoptimized: true, // 對於靜態導出，禁用 Next.js 圖片優化
  },
  env: {
    API_BASE_URL: process.env.API_BASE_URL || 'http://localhost:8000',
  },
};

module.exports = nextConfig;