#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

# 前端部分
echo "🔍 Running frontend checks..."

# 1. 代碼格式檢查
npm run prettier -- --check
if [ $? -ne 0 ]; then
  echo "❌ 代碼格式不符合規範，請運行 npm run prettier 自動修復"
  exit 1
fi

# 2. ESLint 檢查
npm run lint
if [ $? -ne 0 ]; then
  echo "❌ ESLint 檢查失敗，請修復代碼"
  exit 1
fi

# 3. 🔑 單元測試（必須通過）
echo "🧪 Running frontend tests..."
npm run test:coverage
if [ $? -ne 0 ]; then
  echo "❌ 前端測試失敗！提交已阻止！"
  echo "   請修復測試後重試"
  exit 1
fi

echo "✅ 所有前端檢查通過！"
