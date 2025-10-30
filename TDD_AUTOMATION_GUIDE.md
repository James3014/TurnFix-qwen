# TDD 自動化開發流程指南

**日期**：2025-10-28
**目的**：建立自動化 TDD 流程，確保「先寫測試，測試通過才寫代碼」的工程紀律

---

## 🎯 TDD 開發循環

### 傳統三步迴圈
```
1. ❌ RED：寫一個失敗的測試
2. 🟢 GREEN：寫最少代碼讓測試通過
3. 🔵 REFACTOR：改進代碼，保持測試通過
```

### 自動化要點
- **自動檢查**：測試必須先寫，且必須先失敗
- **自動執行**：每次提交前自動運行所有測試
- **自動阻止**：未通過測試的代碼無法合併到 main

---

## 📋 完整的自動化 TDD 工作流

### 步驟 1：本地開發環境配置

#### A. 安裝依賴

**後端（Python）**
```bash
# 在 requirements-dev.txt 中
pytest>=7.0
pytest-cov>=4.0          # 代碼覆蓋率
pytest-asyncio>=0.20     # 異步測試
pytest-mock>=3.10        # Mock 和 Spy
black>=23.0              # 代碼格式化
flake8>=6.0              # 代碼檢查
mypy>=1.0                # 類型檢查

# 安裝
pip install -r requirements-dev.txt
```

**前端（TypeScript/React）**
```bash
# package.json 中
"devDependencies": {
  "jest": "^29.0",
  "@testing-library/react": "^14.0",
  "@testing-library/jest-dom": "^6.0",
  "ts-jest": "^29.0",
  "typescript": "^5.0"
}

npm install
```

#### B. 配置測試框架

**後端 - pytest.ini**
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
  --cov=backend
  --cov-report=html
  --cov-report=term-missing
  --cov-fail-under=80
  -v
```

**前端 - jest.config.js**
```javascript
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  roots: ['<rootDir>/src'],
  testMatch: ['**/__tests__/**/*.ts?(x)', '**/?(*.)+(spec|test).ts?(x)'],
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/index.tsx'
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  }
};
```

---

### 步驟 2：開發流程自動化（Git Hooks）

#### A. 安裝 Git Hooks 框架

```bash
pip install pre-commit
npm install husky --save-dev
npm install lint-staged --save-dev
```

#### B. 配置 Pre-commit Hook（測試必須通過）

**後端 - .pre-commit-config.yaml**
```yaml
repos:
  # 檢查代碼格式
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
        language_version: python3.11

  # 檢查代碼質量
  - repo: https://github.com/PyCQA/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=100']

  # 類型檢查
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.0.0
    hooks:
      - id: mypy
        additional_dependencies: ['types-all']

  # 🔑 運行單元測試（必須通過）
  - repo: local
    hooks:
      - id: pytest-check
        name: pytest
        entry: pytest
        language: system
        types: [python]
        stages: [commit]
        pass_filenames: false
        always_run: true
        verbose: true

install_framework: pre-commit
```

**激活 Hook**
```bash
pre-commit install
pre-commit run --all-files  # 首次運行所有檢查
```

**前端 - .husky/pre-commit**
```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

# 1. 檢查代碼格式
npm run prettier -- --check

# 2. 運行 ESLint
npm run lint

# 3. 🔑 運行單元測試（必須通過）
npm run test:coverage

# 如果測試失敗，退出 hook，阻止提交
if [ $? -ne 0 ]; then
  echo "❌ 測試失敗，提交已阻止！"
  exit 1
fi
```

**安裝 Husky**
```bash
npx husky install
npx husky add .husky/pre-commit "npm run test:coverage"
```

#### C. 配置 Commit Message Hook（檢查提交訊息規範）

**後端和前端 - .husky/commit-msg**
```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

# 檢查提交訊息格式：test: / feat: / fix: / refactor: 等
if ! grep -qE "^(test|feat|fix|refactor|docs|style|perf|chore):" "$1"; then
  echo "❌ 提交訊息必須以以下前綴開頭："
  echo "   test:     新增或修改測試"
  echo "   feat:     新增功能"
  echo "   fix:      修復 bug"
  echo "   refactor: 重構代碼"
  echo "   docs:     更新文檔"
  exit 1
fi
```

---

### 步驟 3：分支保護和 CI/CD 檢查

#### A. GitHub 分支保護規則

**設置路徑**：Repository Settings → Branches → Branch Protection Rules

**main 分支保護規則**：
```
✅ Require a pull request before merging
   ✅ Require approvals (最少 1 個)
   ✅ Require status checks to pass before merging
      - All tests must pass
      - Code coverage must be > 80%
      - No merge conflicts

✅ Require code to be up to date before merging

✅ Include administrators (管理員也受同樣規則限制)
```

#### B. GitHub Actions CI/CD 配置

**後端 - .github/workflows/backend-tests.yml**
```yaml
name: Backend Tests

on:
  push:
    branches: [main, develop]
    paths:
      - 'backend/**'
      - 'tests/**'
      - '.github/workflows/backend-tests.yml'
  pull_request:
    branches: [main, develop]
    paths:
      - 'backend/**'
      - 'tests/**'

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Lint with flake8
        run: |
          flake8 backend --count --select=E9,F63,F7,F82 --show-source --statistics
          flake8 backend --count --exit-zero --max-complexity=10 --max-line-length=100

      - name: Type check with mypy
        run: mypy backend

      - name: 🔑 Run tests with pytest
        run: |
          pytest --cov=backend --cov-report=xml --cov-report=html

      - name: Check coverage threshold
        run: |
          coverage report --fail-under=80

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: true

      - name: Archive test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-results-${{ matrix.python-version }}
          path: htmlcov/
```

**前端 - .github/workflows/frontend-tests.yml**
```yaml
name: Frontend Tests

on:
  push:
    branches: [main, develop]
    paths:
      - 'frontend/**'
      - '.github/workflows/frontend-tests.yml'
  pull_request:
    branches: [main, develop]
    paths:
      - 'frontend/**'

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Format check
        run: npm run prettier -- --check

      - name: 🔑 Run tests with coverage
        run: npm run test:coverage

      - name: Archive coverage
        uses: actions/upload-artifact@v3
        with:
          name: coverage-report
          path: coverage/
```

---

## 🔄 TDD 開發工作流

### 日常開發流程

```
1️⃣ 創建功能分支
   $ git checkout -b test/feature-name

2️⃣ 寫第一個失敗測試
   $ cat > tests/test_new_feature.py
   def test_should_do_something():
       # Given
       # When
       # Then
       assert ...

3️⃣ 運行測試（確認失敗）
   $ pytest tests/test_new_feature.py -v
   ❌ FAILED test_new_feature.py::test_should_do_something

4️⃣ 寫最少代碼讓測試通過
   $ cat > backend/feature.py
   def do_something():
       return expected_result

5️⃣ 運行測試（確認通過）
   $ pytest tests/test_new_feature.py -v
   ✅ PASSED test_new_feature.py::test_should_do_something

6️⃣ 提交代碼（Pre-commit hook 會自動運行所有測試）
   $ git add tests/test_new_feature.py backend/feature.py
   $ git commit -m "test: add test for new feature"

   ✅ Running pytest-check...
   ✅ All tests passed (156 tests)
   ✅ Coverage: 83.2% (threshold: 80%)

7️⃣ 重構代碼（如需要）
   $ # 改進代碼，保持測試通過

8️⃣ 創建 Pull Request
   $ git push origin test/feature-name
   $ # 在 GitHub 創建 PR

9️⃣ CI/CD 自動檢查
   ✅ Backend tests passed (3.9, 3.10, 3.11)
   ✅ Frontend tests passed
   ✅ Coverage: 83.2% (> 80%)
   ✅ No merge conflicts

🔟 審批和合併
   $ # 至少 1 個人審批
   $ git merge test/feature-name
   ✅ 自動部署到 staging
```

---

## 📊 測試結構範例

### 後端 - API 層測試

**目錄結構**
```
backend/
├── api/
│   ├── feedback.py          # API 端點
│   └── __init__.py
└── tests/
    ├── test_feedback_api.py # API 測試
    ├── conftest.py          # Fixtures
    └── __init__.py
```

**tests/conftest.py - 共用 Fixtures**
```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.db import Base
from backend.main import app

@pytest.fixture
def test_db():
    """建立測試數據庫"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    yield db
    db.close()

@pytest.fixture
def client(test_db):
    """建立測試客戶端"""
    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def sample_session():
    """建立示例 Session"""
    return {
        "id": 1,
        "user_id": 1,
        "symptom_id": 1,
        "chosen_cards": [1, 2, 3]
    }
```

**tests/test_feedback_api.py - API 測試**
```python
import pytest

class TestPracticeCardFeedback:

    def test_submit_star_rating_should_save_correctly(self, client, sample_session):
        """給練習卡評分應該正確保存"""
        # 前置條件：創建會話和練習卡
        # ...

        # 執行：POST 評分
        response = client.post(
            "/api/v1/feedback/practice-card",
            json={
                "session_id": sample_session["id"],
                "practice_id": 1,
                "rating": 4,
                "comment": "清晰有幫助"
            }
        )

        # 驗證：響應正確
        assert response.status_code == 201
        assert response.json()["rating"] == 4
        assert response.json()["is_favorite"] == False

        # 驗證：數據已保存到數據庫
        feedback = get_practice_card_feedback(sample_session["id"], 1)
        assert feedback.rating == 4
        assert feedback.comment == "清晰有幫助"

    def test_favorite_should_be_independent_of_rating(self, client):
        """加入最愛應該獨立於評分"""
        # 給卡片評分
        client.post("/api/v1/feedback/practice-card", json={
            "session_id": 1,
            "practice_id": 1,
            "rating": 2
        })

        # 加入最愛（獨立操作）
        response = client.put(
            "/api/v1/feedback/practice-card/1",
            json={"is_favorite": True}
        )

        assert response.status_code == 200
        feedback = response.json()
        assert feedback["rating"] == 2
        assert feedback["is_favorite"] == True
```

### 前端 - UI 組件測試

**tests/components/StarRating.test.tsx**
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { StarRating } from '@/components/StarRating';

describe('StarRating Component', () => {

  it('should display 5 stars', () => {
    render(<StarRating onRate={() => {}} />);
    const stars = screen.getAllByRole('button', { name: /star/i });
    expect(stars).toHaveLength(5);
  });

  it('should call onRate with correct value when clicking', () => {
    const onRate = jest.fn();
    render(<StarRating onRate={onRate} />);

    const stars = screen.getAllByRole('button', { name: /star/i });
    fireEvent.click(stars[3]); // Click 4th star

    expect(onRate).toHaveBeenCalledWith(4);
  });

  it('should show meaning when rating is selected', () => {
    const { rerender } = render(<StarRating value={4} onRate={() => {}} />);

    expect(screen.getByText('你評分了 4 顆星 - 適用')).toBeInTheDocument();
  });

  it('should support independent favorite toggle', () => {
    const onFavorite = jest.fn();
    render(<StarRating value={3} onRate={() => {}} onFavorite={onFavorite} />);

    const favoriteBtn = screen.getByRole('button', { name: /加入最愛/i });
    fireEvent.click(favoriteBtn);

    expect(onFavorite).toHaveBeenCalledWith(true);
  });
});
```

---

## 📈 測試覆蓋率要求

### 分層覆蓋率標準

| 層級 | 最小要求 | 目標 | 說明 |
|------|---------|------|------|
| **業務邏輯** (Service) | 90% | 95% | 核心邏輯必須高度覆蓋 |
| **API 端點** (Controller) | 85% | 90% | 確保接口行為正確 |
| **UI 組件** (Component) | 80% | 85% | 交互和渲染邏輯 |
| **Util 函數** | 80% | 90% | 邊界情況要測 |
| **整體** | 80% | 85% | 全項目門檻 |

### 檢查覆蓋率

**後端**
```bash
# 生成 HTML 報告
pytest --cov=backend --cov-report=html

# 查看終端報告
pytest --cov=backend --cov-report=term-missing

# 檢查是否達到門檻
coverage report --fail-under=80
```

**前端**
```bash
npm run test:coverage

# 查看覆蓋率報告
open coverage/lcov-report/index.html
```

---

## 🚨 質量閘門（Quality Gates）

### 分支推送前檢查（Pre-commit）

```
✅ 代碼格式化 (Prettier/Black)
✅ 代碼檢查 (ESLint/Flake8)
✅ 類型檢查 (TypeScript/mypy)
✅ 單元測試全部通過
✅ 覆蓋率 ≥ 80%
✅ 沒有安全漏洞
```

### 創建 PR 時檢查（GitHub Actions）

```
✅ 所有平台上的測試通過 (3.9, 3.10, 3.11)
✅ 端到端測試通過
✅ 性能測試通過
✅ 代碼審查通過（至少 1 人）
✅ 無合併衝突
```

### 合併前檢查（Branch Protection）

```
✅ 所有 CI/CD 檢查通過
✅ 至少 1 個批准
✅ 代碼最新 (up to date)
✅ 無衝突
```

---

## 📋 TDD 檢查清單

### 開發新功能時

- [ ] **Day 1：寫測試**
  - [ ] 寫失敗的單元測試（TEST-RED）
  - [ ] 確認測試確實失敗
  - [ ] 提交：`git commit -m "test: add test for feature X"`

- [ ] **Day 2-3：寫代碼**
  - [ ] 寫最少代碼讓測試通過（TEST-GREEN）
  - [ ] 運行測試確認通過
  - [ ] 提交：`git commit -m "feat: implement feature X"`

- [ ] **Day 4：重構**
  - [ ] 改進代碼質量（REFACTOR）
  - [ ] 確保測試仍通過
  - [ ] 提交：`git commit -m "refactor: improve feature X"`

- [ ] **Day 5：提交 PR**
  - [ ] 本地測試 100% 通過
  - [ ] 覆蓋率 ≥ 80%
  - [ ] 提交 PR：`git push origin feature-x`

- [ ] **Code Review**
  - [ ] 至少 1 人審批
  - [ ] GitHub Actions 全部通過
  - [ ] 合併到 main

---

## 🔧 故障排除

### 問題 1：Pre-commit hook 執行過慢

**原因**：測試數量多或涉及 I/O

**解決**：
```bash
# 方案 A：並行運行測試
pytest -n 4  # 使用 4 核心

# 方案 B：只運行相關測試
pytest tests/test_feedback_api.py -k "not slow"

# 方案 C：配置 hook 跳過某些檢查
# .pre-commit-config.yaml
stages: [commit]  # 只在 commit 時運行，不在 push
```

### 問題 2：CI/CD 中測試失敗但本地通過

**原因**：
1. 環境變量不同
2. Python 版本不同
3. 時序相關的 bug

**解決**：
```bash
# 本地模擬 CI 環境
python3.9 -m pytest  # 指定版本

# 檢查環境變量
echo $DATABASE_URL

# 運行特定測試多次
pytest test_api.py -v --count=10
```

### 問題 3：被迫跳過 Hook 提交

**絕對不要做這個**！
```bash
# ❌ 不要使用
git commit --no-verify

# ✅ 應該做的
# 1. 修復失敗的測試
# 2. 或者在 PR 中解釋為什麼跳過
```

---

## 📈 度量和監控

### 建立 TDD 儀表板

**指標追蹤**
```
📊 測試覆蓋率趨勢
   - 目標：80%+，理想 85%+
   - 警告：< 80% 無法合併

📊 測試執行時間
   - 目標：< 30 秒（本地）
   - 目標：< 5 分鐘（CI/CD）

📊 失敗率
   - 目標：< 1%（偶發性 bug）
   - 警告：> 5%（系統性問題）

📊 代碼審查時間
   - 目標：24 小時內審批
   - 目標：7 天內合併
```

### 每周報告

```
這周 TDD 指標：
✅ 測試覆蓋率：83.2% (↑ 2.1% from last week)
✅ 測試執行時間：28s (本地), 4m20s (CI)
✅ 失敗率：0.8%
✅ PR 平均審批時間：18 小時
✅ Bug 發現時間：95% 在開發階段（測試發現）

問題和改進：
- 某些集成測試偶發超時，需優化
- 前端測試覆蓋率 76%，目標 80%
```

---

## 🎓 TDD 最佳實踐

### 1. 遵循 Given-When-Then 模式

```python
def test_should_save_feedback_correctly():
    # Given - 前置條件
    session = create_sample_session()
    card = create_sample_card()

    # When - 執行操作
    feedback = submit_rating(session, card, rating=4)

    # Then - 驗證結果
    assert feedback.rating == 4
    assert feedback.is_favorite == False
```

### 2. 一個測試只測一個東西

```python
# ❌ 不好：測試多個行為
def test_feedback():
    feedback = create_feedback(rating=4)
    assert feedback.rating == 4
    assert feedback.is_saved == True
    assert feedback.timestamp is not None

# ✅ 好：分開測試
def test_should_set_rating():
    feedback = create_feedback(rating=4)
    assert feedback.rating == 4

def test_should_save_to_db():
    feedback = create_feedback()
    assert feedback.is_saved == True

def test_should_record_timestamp():
    feedback = create_feedback()
    assert feedback.timestamp is not None
```

### 3. 使用有意義的測試名稱

```python
# ❌ 不好
def test_1():
    ...

# ✅ 好：能清楚看出在測什麼
def test_should_prevent_duplicate_favorite_entries():
    ...

def test_rating_should_be_integer_between_1_and_5():
    ...

def test_concurrent_feedback_submissions_should_not_race():
    ...
```

### 4. Mock 外部依賴

```python
def test_should_call_notification_api():
    """當評分提交時，應該調用通知 API"""
    with mock.patch('backend.notifications.send_email') as mock_send:
        submit_feedback(session_id=1, rating=5)

        # 驗證調用
        mock_send.assert_called_once()
        args = mock_send.call_args
        assert "feedback" in args.kwargs
```

### 5. 測試邊界情況

```python
def test_rating_validation():
    # 邊界情況
    assert is_valid_rating(1) == True   # 最小值
    assert is_valid_rating(5) == True   # 最大值
    assert is_valid_rating(0) == False  # 低於最小
    assert is_valid_rating(6) == False  # 高於最大
    assert is_valid_rating(None) == False
    assert is_valid_rating("4") == False
```

---

## 🚀 實施時間表

### 第 0 周：準備環境
- [ ] 安裝測試框架和工具
- [ ] 配置 pytest 和 jest
- [ ] 設置 Git hooks (pre-commit, husky)
- [ ] 配置 GitHub Actions 工作流
- [ ] 設置分支保護規則

### 第 1 周：TDD 實踐開始
- [ ] 團隊培訓（2 小時）
- [ ] 編寫前 5 個功能的測試
- [ ] 確認 hook 正常工作
- [ ] 檢查覆蓋率達到 70%+

### 第 2-3 周：深化實踐
- [ ] 所有功能遵循 TDD
- [ ] 覆蓋率達到 80%+
- [ ] 建立代碼審查流程
- [ ] 優化測試執行時間

### 第 4 周+：維護和優化
- [ ] 維持 80%+ 覆蓋率
- [ ] 持續優化測試速度
- [ ] 監控和改進工作流

---

## 💡 常見問題

### Q: TDD 是否會減慢開發速度？

**A**: 短期可能，長期加快。
- 第 1-2 周：速度 -20%（習慣適應）
- 第 3-4 周：速度 0%（持平）
- 第 5 周+：速度 +30%（減少 debug 時間）

### Q: 如何處理遺留代碼？

**A**: 分階段改進
- 新功能：100% TDD
- 修改舊代碼：添加測試後再改
- 逐步覆蓋到 80%

### Q: 測試失敗很頻繁怎麼辦？

**A**:
1. 檢查測試是否寫得過度
2. Mock 外部依賴
3. 增加重試機制處理偶發故障
4. 優化測試的隔離性

---

**版本**：v1.0
**推薦開始**：第 0 周末或第 1 周初
**成功標誌**：80%+ 測試覆蓋率，0 個測試失敗在合併前被發現

祝 TDD 實踐順利！🎯
