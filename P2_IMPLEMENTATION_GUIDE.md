# P2 長期改進實施指南

本文檔說明如何完成 P2 級別的長期改進任務。基礎配置文件已創建,但需要進一步配置和遷移。

## 已創建的配置文件

### 前端工具鏈
- `tsconfig.json` - TypeScript 配置
- `.eslintrc.json` - ESLint 配置
- `.prettierrc.json` - Prettier 配置

### 後端工具鏈
- `backend/pyproject.toml` - Black, isort, pytest 配置

### CI/CD
- `.github/workflows/ci.yml` - GitHub Actions 工作流
- `.pre-commit-config.yaml` - Pre-commit hooks 配置

## 待完成任務

### TypeScript 遷移 (P2-1 to P2-4)

**所需步驟:**
```bash
# 1. 安裝 TypeScript 相關依賴
npm install --save-dev typescript @types/react @types/react-dom @types/react-router-dom @types/node

# 2. 逐步遷移文件
# - 從 .js 重命名為 .tsx (組件) 或 .ts (工具/API)
# - 添加類型定義
# - 修復類型錯誤

# 建議遷移順序:
# 1. src/api/client.js → client.ts
# 2. src/hooks/*.js → *.ts
# 3. src/components/common/*.js → *.tsx
# 4. src/components/*.js → *.tsx
```

### 測試框架 (P2-5 to P2-10)

**後端測試:**
```bash
# 1. 安裝測試依賴
cd backend
pip install pytest pytest-cov pytest-asyncio httpx

# 2. 創建測試目錄結構
mkdir -p tests/{unit,integration}
mkdir -p tests/unit/{repositories,services}
mkdir -p tests/integration/api

# 3. 編寫測試
# 範例: tests/unit/repositories/test_symptom_repository.py
# 範例: tests/integration/api/test_symptoms.py

# 4. 運行測試
pytest --cov=backend --cov-report=html
```

**前端測試:**
```bash
# 1. 安裝測試依賴
npm install --save-dev @testing-library/react @testing-library/jest-dom @testing-library/user-event vitest jsdom

# 2. 創建測試配置
# - 添加 vitest.config.js
# - 設置 setupTests.js

# 3. 編寫測試
# 範例: src/hooks/__tests__/usePracticeCards.test.js
# 範例: src/components/__tests__/PracticeCardManagement.test.js

# 4. 運行測試
npm run test
```

### 代碼格式化 (P2-12 to P2-13)

**前端 (已配置):**
```bash
# 安裝依賴
npm install --save-dev eslint prettier eslint-plugin-react eslint-plugin-react-hooks

# 格式化代碼
npx prettier --write src
npx eslint src --fix
```

**後端 (已配置):**
```bash
# 安裝依賴
pip install black isort

# 格式化代碼
black backend
isort backend
```

### Pre-commit Hooks (P2-14)

```bash
# 1. 安裝 pre-commit
pip install pre-commit

# 2. 安裝 hooks
pre-commit install

# 3. 首次運行
pre-commit run --all-files
```

### CI/CD (P2-15)

GitHub Actions 工作流已創建在 `.github/workflows/ci.yml`。

**啟用步驟:**
1. Push 代碼到 GitHub
2. 進入 Repository Settings → Actions → Enable workflows
3. 每次 push/PR 會自動觸發

### API 文檔 (P2-11)

FastAPI 自動生成文檔,訪問:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

**改進建議:**
1. 為所有端點添加詳細的 docstring
2. 使用 Pydantic models 的 `Field()` 添加描述
3. 添加示例請求/響應

### 代碼覆蓋率 (P2-16)

**後端:**
```bash
pytest --cov=backend --cov-report=html --cov-report=term
# 報告生成在 htmlcov/index.html
```

**前端:**
```bash
npm run test -- --coverage
# 報告生成在 coverage/index.html
```

## 實施優先級

1. **立即執行 (高影響):**
   - Pre-commit hooks (P2-14)
   - 代碼格式化工具 (P2-12, P2-13)

2. **短期 (1-2 週):**
   - 後端單元測試 (P2-5, P2-6)
   - 前端測試框架 (P2-8)

3. **中期 (1-2 個月):**
   - TypeScript 遷移 (P2-1 to P2-4)
   - API 集成測試 (P2-7)
   - 組件測試 (P2-9, P2-10)

4. **持續改進:**
   - CI/CD pipeline (P2-15)
   - 代碼覆蓋率監控 (P2-16)

## 預期效益

- **代碼品質:** ESLint/Prettier/Black 確保一致性
- **類型安全:** TypeScript 減少運行時錯誤
- **測試覆蓋:** pytest/vitest 提高信心
- **自動化:** CI/CD 加速開發流程
- **文檔:** 自動生成的 API 文檔

## 注意事項

1. TypeScript 遷移應**逐步進行**,避免一次性重構
2. 測試應**先寫核心功能**,然後擴展到邊緣情況
3. CI/CD 配置可能需要根據實際部署環境調整
4. Pre-commit hooks 會在提交時自動格式化代碼,初期可能較慢

---

**狀態:** 基礎配置已完成,可開始逐步實施各項任務
