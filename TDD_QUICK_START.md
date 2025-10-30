# TDD 自動化 - 快速開始指南

**時間**：15 分鐘設置，獲得完整的自動化 TDD 工作流
**目標**：確保測試通過才能提交/合併代碼

---

## 📦 安裝（5 分鐘）

### 後端設置

```bash
# 1. 進入後端目錄
cd backend

# 2. 安裝測試和檢查工具
pip install -r requirements-dev.txt

# 3. 安裝 pre-commit hooks
pre-commit install

# 4. 驗證 hooks 正確安裝
pre-commit run --all-files
```

### 前端設置

```bash
# 1. 進入前端目錄
cd frontend

# 2. 安裝依賴（包含測試工具）
npm install

# 3. 安裝 Husky
npx husky install

# 4. 添加 pre-commit hook
npx husky add .husky/pre-commit "npm run test:coverage"

# 5. 驗證安裝
npm run test:coverage
```

---

## ✅ 驗證安裝

### 測試 Hooks 是否生效

```bash
# 1. 在任何 Python 文件中添加一個簡單的改動
echo "# test" >> backend/test.py

# 2. 嘗試提交
git add backend/test.py
git commit -m "test: verify hooks"

# 預期：Hook 會自動運行測試
# ✅ 成功：顯示所有檢查通過
# ❌ 失敗：顯示測試失敗，提交被阻止
```

---

## 🔄 日常開發工作流

### 開發新功能的完整流程

```bash
# 第 1 步：創建功能分支
git checkout -b test/my-feature

# 第 2 步：寫第一個測試（必須失敗）
cat > tests/test_my_feature.py << 'EOF'
def test_should_do_something():
    result = my_function()
    assert result == expected_value
EOF

# 第 3 步：驗證測試失敗
pytest tests/test_my_feature.py
# ❌ FAILED

# 第 4 步：寫實現代碼
cat > backend/my_feature.py << 'EOF'
def my_function():
    return expected_value
EOF

# 第 5 步：運行測試確認通過
pytest tests/test_my_feature.py
# ✅ PASSED

# 第 6 步：提交（Hook 會自動運行所有測試）
git add .
git commit -m "test: add test for my feature"
# Hook 自動運行...
# ✅ 所有檢查通過，提交成功！

# 第 7 步：推送並創建 PR
git push origin test/my-feature
# GitHub Actions 自動運行所有檢查
```

---

## 🛑 常見操作

### 運行所有測試

**後端**
```bash
# 運行所有後端測試
pytest tests/ -v

# 運行特定測試
pytest tests/test_feedback_api.py -v

# 運行並查看覆蓋率
pytest tests/ --cov=backend --cov-report=html
# 在瀏覽器打開：htmlcov/index.html
```

**前端**
```bash
# 運行所有前端測試
npm test

# 運行特定測試
npm test -- StarRating

# 運行並查看覆蓋率
npm run test:coverage
# 在瀏覽器打開：coverage/lcov-report/index.html
```

### 檢查代碼質量

**後端**
```bash
# 檢查代碼格式
black --check backend

# 自動格式化
black backend

# 檢查代碼風格
flake8 backend

# 類型檢查
mypy backend
```

**前端**
```bash
# 檢查格式
npm run prettier -- --check

# 自動格式化
npm run prettier

# 檢查代碼質量
npm run lint
```

### 手動運行 Hooks（不提交）

```bash
# 後端
pre-commit run --all-files

# 前端
npm run test:coverage && npm run lint
```

---

## 🚨 如果測試失敗

### 情況 1：本地測試失敗

```bash
# 1. 看錯誤訊息，了解失敗原因
pytest tests/test_my_feature.py -v

# 2. 修復代碼
# ... 編輯 backend/my_feature.py ...

# 3. 重新運行測試
pytest tests/test_my_feature.py -v

# 4. 確認通過後提交
git add .
git commit -m "fix: resolve test failure"
```

### 情況 2：Hook 阻止提交

```
❌ 提交被阻止：測試未通過

# 修復步驟：
1. 查看錯誤訊息
2. 修復代碼或測試
3. 運行 pytest 確認通過
4. 重新提交
```

### 情況 3：CI/CD 失敗

```
# 如果 GitHub Actions 失敗：
1. 點擊 GitHub PR 中的 "Details"
2. 查看失敗的日誌
3. 本地修復
4. 重新推送（自動重新運行 CI）
```

### 情況 4：被迫需要跳過 Hook

```bash
# ❌ 絕對不要做這個
git commit --no-verify

# ✅ 應該做的
# 1. 修復失敗的測試
# 2. 或者在 PR 中解釋為什麼需要特殊處理
```

---

## 📊 查看測試覆蓋率

### 生成覆蓋率報告

**後端**
```bash
pytest tests/ --cov=backend --cov-report=html
open htmlcov/index.html
```

**前端**
```bash
npm run test:coverage
open coverage/lcov-report/index.html
```

### 目標覆蓋率

- **最小要求**：80%
- **理想目標**：85%+
- **核心邏輯**：90%+

---

## 🔧 自定義配置

### 修改覆蓋率門檻

**後端 - pytest.ini**
```ini
[pytest]
addopts =
  --cov-fail-under=85  # 改為 85%
```

**前端 - jest.config.js**
```javascript
coverageThreshold: {
  global: {
    lines: 85,  // 改為 85%
  }
}
```

### 排除某些文件

**後端 - pytest.ini**
```ini
[pytest]
testpaths = tests
python_files = test_*.py
```

**前端 - jest.config.js**
```javascript
collectCoverageFrom: [
  'src/**/*.{ts,tsx}',
  '!src/**/*.d.ts',           // 排除類型定義
  '!src/index.tsx',           // 排除入口文件
  '!src/generated/**',        // 排除生成的文件
]
```

---

## 🎯 故障排除

### 問題：Pre-commit hook 執行太慢

**症狀**：提交時需要等待 1-2 分鐘

**解決**：
```bash
# 方案 A：並行運行測試
# pytest.ini 中添加
addopts = -n auto  # 使用所有 CPU 核心

# 方案 B：優化測試
# 分離快速和慢速測試
pytest tests/ -m "not slow"

# 方案 C：禁用某些檢查
# .pre-commit-config.yaml 中註釋掉 mypy
```

### 問題：本地通過但 CI 失敗

**症狀**：GitHub Actions 顯示測試失敗，但本地通過

**解決**：
```bash
# 1. 檢查 Python 版本
python --version  # 應該是 3.9, 3.10, 或 3.11

# 2. 檢查環境變量
export DATABASE_URL="sqlite:///test.db"

# 3. 清除本地緩存並重新運行
rm -rf .pytest_cache
pytest tests/ --tb=short
```

### 問題：無法跳過 Hook

**症狀**：想提交但 Hook 阻止了

**解決**：
```bash
# ❌ 不要用
git commit --no-verify

# ✅ 正確做法
# 1. 修復失敗的測試
pytest tests/ -v

# 2. 更新代碼
# ... 編輯文件 ...

# 3. 重新提交
git add .
git commit -m "fix: resolve test failures"
```

---

## 📚 進階用法

### 使用 Test Markers（標記）

```python
# tests/test_api.py
import pytest

@pytest.mark.slow
def test_api_performance():
    # 這個測試會很慢
    ...

@pytest.mark.unit
def test_simple_function():
    # 快速單元測試
    ...

# 運行
pytest -m unit      # 只運行 unit 測試
pytest -m "not slow"  # 跳過 slow 測試
```

### 並行運行測試

```bash
# 安裝
pip install pytest-xdist

# 運行（使用 4 個 workers）
pytest -n 4
```

### 監視文件變化自動運行測試

```bash
# 安裝
pip install pytest-watch

# 運行
ptw  # 文件一旦保存，自動運行相關測試
```

---

## ✨ 最佳實踐

### 1. 一個提交 = 一個功能 + 測試

```bash
# ✅ 好的提交
commit 1: test: add test for feature X
commit 2: feat: implement feature X
commit 3: refactor: improve feature X

# ❌ 避免
commit 1: feat: add feature X, Y, Z with tests
```

### 2. 測試名稱要有意義

```python
# ❌ 不好
def test_1():
    ...

# ✅ 好
def test_should_save_feedback_with_correct_rating():
    ...
```

### 3. 一個測試只測一個東西

```python
# ❌ 不好
def test_feedback():
    assert feedback.rating == 4
    assert feedback.is_saved == True

# ✅ 好
def test_should_set_rating():
    assert feedback.rating == 4

def test_should_save_to_db():
    assert feedback.is_saved == True
```

---

## 🚀 下一步

1. **現在就試試**：
   ```bash
   # 後端
   cd backend && pip install -r requirements-dev.txt && pre-commit install

   # 前端
   cd frontend && npm install && npx husky install
   ```

2. **寫第一個測試**：
   - 參考 TDD_AUTOMATION_GUIDE.md 的「測試結構範例」
   - 寫一個簡單的功能測試

3. **提交並觀察**：
   - Hook 會自動運行
   - GitHub Actions 會自動檢查

4. **持續學習**：
   - 查閱 TDD_AUTOMATION_GUIDE.md 了解更多細節
   - 參考項目中的現有測試

---

## 📞 常見問題速查

| 問題 | 解決方案 |
|------|---------|
| Hook 太慢 | 使用 `pytest -n auto` 並行運行 |
| 本地通過 CI 失敗 | 檢查 Python 版本和環境變量 |
| 需要跳過 Hook | 修復測試，不要用 `--no-verify` |
| 不知道寫什麼測試 | 查看 TDD_AUTOMATION_GUIDE.md 的範例 |
| 測試失敗不知道原因 | 加 `-v` 看詳細輸出：`pytest -v` |

---

**版本**：v1.0
**更新**：2025-10-28
**狀態**：✅ 可立即使用

祝你 TDD 之旅順利！🚀
