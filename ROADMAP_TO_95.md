# TurnFix-qwen 95 分達成計劃

**目標**: 從目前的 75-80 分提升到 95 分
**預計時間**: 3-5 天全職工作
**當前狀態**: 75/100

---

## 📊 提升計劃概覽

| 階段 | 任務 | 預計提升 | 優先級 | 時間 |
|------|------|----------|--------|------|
| Phase 1 | 後端測試 (70% 覆蓋) | +10 分 | ⭐⭐⭐ 必須 | 6-8 小時 |
| Phase 2 | 前端測試 (60% 覆蓋) | +5 分 | ⭐⭐⭐ 必須 | 4-6 小時 |
| Phase 3 | 安全機制 (JWT + 權限) | +5 分 | ⭐⭐⭐ 必須 | 4-5 小時 |
| Phase 4 | 完成剩餘重構 | +3 分 | ⭐⭐ 重要 | 2-3 小時 |
| Phase 5 | 錯誤處理和日誌 | +2 分 | ⭐⭐ 重要 | 2-3 小時 |
| Phase 6 | Docker 部署配置 | +3 分 | ⭐⭐ 重要 | 3-4 小時 |
| Phase 7 | 完善文檔 | +2 分 | ⭐ 可選 | 2-3 小時 |
| Phase 8 | 最終驗證 | - | ⭐⭐⭐ 必須 | 1-2 小時 |

**預計總時間**: 24-34 小時
**目標總分**: 95-100/100

---

## 📋 Phase 1: 後端測試覆蓋 (70%) [+10 分]

### 目標
- 達到 70% 後端代碼測試覆蓋率
- 所有核心功能有單元測試和集成測試
- CI/CD 自動運行測試

### 任務清單

#### 1.1 設置測試框架 (30分鐘)
```bash
# 安裝依賴
pip install pytest pytest-cov pytest-asyncio httpx faker

# 創建測試目錄結構
mkdir -p backend/tests/{unit,integration}
mkdir -p backend/tests/unit/{repositories,services}
mkdir -p backend/tests/integration/api
```

**文件**: `backend/tests/conftest.py`
```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def test_db():
    """測試資料庫 fixture"""
    # 使用 SQLite in-memory
    engine = create_engine("sqlite:///:memory:")
    # 創建表格
    # ...

@pytest.fixture
def client(test_db):
    """測試客戶端 fixture"""
    from backend.main import app
    return TestClient(app)
```

#### 1.2 Repository 層單元測試 (2小時)
**優先級**: ⭐⭐⭐

測試文件:
- `tests/unit/repositories/test_symptom_repository.py`
- `tests/unit/repositories/test_practice_card_repository.py`
- `tests/unit/repositories/test_feedback_repository.py`

測試覆蓋:
- ✓ CRUD 操作
- ✓ 查詢方法
- ✓ 錯誤處理
- ✓ 邊界情況

**範例** (`test_symptom_repository.py`):
```python
def test_create_symptom(test_db):
    repo = SymptomRepository(test_db)
    symptom = repo.create(SymptomCreate(
        name="重心太後",
        category="技術",
        synonyms=["後坐"]
    ))
    assert symptom.id is not None
    assert symptom.name == "重心太後"

def test_get_symptom_by_id(test_db):
    # ...

def test_delete_symptom(test_db):
    # ...
```

#### 1.3 API 端點集成測試 (3小時)
**優先級**: ⭐⭐⭐

測試文件:
- `tests/integration/api/test_admin_symptoms.py`
- `tests/integration/api/test_admin_practice_cards.py`
- `tests/integration/api/test_feedback.py`

測試覆蓋:
- ✓ GET/POST/PUT/DELETE 端點
- ✓ 狀態碼驗證
- ✓ 響應格式驗證
- ✓ 錯誤情況處理

**範例** (`test_admin_symptoms.py`):
```python
def test_create_symptom_api(client):
    response = client.post("/api/v1/admin/symptoms", json={
        "name": "重心太後",
        "category": "技術",
        "synonyms": ["後坐"]
    })
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_get_symptoms_api(client):
    # ...
```

#### 1.4 Service 層測試 (1.5小時)
**優先級**: ⭐⭐

測試文件:
- `tests/unit/services/test_ski_tips_service.py`
- `tests/unit/services/test_video_demo_service.py`

#### 1.5 驗證覆蓋率 (30分鐘)
```bash
pytest --cov=backend --cov-report=html --cov-report=term
# 目標: 70%+ 覆蓋率
```

**成功標準**:
- ✅ 所有測試通過
- ✅ 覆蓋率 >= 70%
- ✅ CI/CD 測試自動運行

---

## 📋 Phase 2: 前端測試覆蓋 (60%) [+5 分]

### 目標
- 達到 60% 前端代碼測試覆蓋率
- 核心 Hooks 和組件有完整測試

### 任務清單

#### 2.1 設置測試框架 (30分鐘)
```bash
# 安裝依賴
npm install --save-dev vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom

# 創建配置
```

**文件**: `vitest.config.js`
```javascript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: './src/setupTests.js',
    coverage: {
      reporter: ['text', 'html'],
      exclude: ['node_modules/', 'src/setupTests.js'],
    },
  },
});
```

#### 2.2 Hooks 單元測試 (2小時)
**優先級**: ⭐⭐⭐

測試文件:
- `src/hooks/__tests__/usePracticeCards.test.js`
- `src/hooks/__tests__/useSymptoms.test.js`
- `src/hooks/__tests__/useFavorites.test.js`

**範例**:
```javascript
import { renderHook, waitFor } from '@testing-library/react';
import { usePracticeCards } from '../usePracticeCards';

test('loads practice cards on mount', async () => {
  const { result } = renderHook(() => usePracticeCards());

  expect(result.current.loading).toBe(true);

  await waitFor(() => {
    expect(result.current.loading).toBe(false);
  });

  expect(result.current.practiceCards.length).toBeGreaterThan(0);
});
```

#### 2.3 組件測試 (2小時)
**優先級**: ⭐⭐

測試文件:
- `src/components/__tests__/PracticeCardManagement.test.js`
- `src/components/__tests__/SymptomManagement.test.js`

#### 2.4 驗證覆蓋率 (30分鐘)
```bash
npm run test -- --coverage
# 目標: 60%+ 覆蓋率
```

**成功標準**:
- ✅ 所有測試通過
- ✅ 覆蓋率 >= 60%
- ✅ CI/CD 測試自動運行

---

## 📋 Phase 3: 安全機制實施 [+5 分]

### 目標
- JWT 認證系統
- 角色權限控制 (admin, user)
- CORS 和安全頭配置

### 任務清單

#### 3.1 JWT 認證 (2.5小時)
**優先級**: ⭐⭐⭐

**新增文件**:
- `backend/core/security.py` - JWT 工具函數
- `backend/api/v1/auth.py` - 認證端點
- `backend/models/user.py` - 用戶模型

**核心功能**:
```python
# backend/core/security.py
from jose import JWTError, jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict) -> str:
    """創建 JWT token"""
    # ...

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """驗證密碼"""
    # ...

def get_current_user(token: str = Depends(oauth2_scheme)):
    """獲取當前用戶"""
    # ...
```

**API 端點**:
- `POST /api/v1/auth/register` - 註冊
- `POST /api/v1/auth/login` - 登入
- `GET /api/v1/auth/me` - 獲取當前用戶

#### 3.2 角色權限控制 (1.5小時)
**優先級**: ⭐⭐⭐

```python
# backend/core/permissions.py
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

def require_role(role: UserRole):
    """角色檢查裝飾器"""
    def decorator(func):
        # ...
    return decorator

# 使用範例
@router.post("/admin/symptoms")
@require_role(UserRole.ADMIN)
async def create_symptom(...):
    # 只有 admin 可以訪問
```

**保護的端點**:
- 所有 `/admin/*` 端點需要 admin 角色
- 用戶數據端點需要認證

#### 3.3 CORS 和安全配置 (1小時)
**優先級**: ⭐⭐

```python
# backend/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 生產環境改為實際域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加安全頭
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response
```

**成功標準**:
- ✅ 用戶可以註冊和登入
- ✅ JWT token 正確生成和驗證
- ✅ Admin 端點受保護
- ✅ CORS 正確配置

---

## 📋 Phase 4: 完成剩餘重構 [+3 分]

### 目標
- 重構最後 2 個大組件
- 所有組件 < 150 行

### 任務清單

#### 4.1 重構 SymptomPracticeMappingManagement (1.5小時)
**優先級**: ⭐⭐

**當前**: 363 行
**目標**: < 100 行

**拆分方案**:
```
SymptomPracticeMappingManagement.js (主組件 ~80行)
  ├── admin/MappingForm.js (~120行)
  └── admin/MappingList.js (~90行)
```

#### 4.2 重構 ReviewInterface (1.5小時)
**優先級**: ⭐⭐

**當前**: 305 行
**目標**: < 100 行

**拆分方案**:
```
ReviewInterface.js (主組件 ~80行)
  ├── review/ReviewCard.js (~100行)
  └── review/ReviewActions.js (~60行)
```

**成功標準**:
- ✅ 所有組件 < 150 行
- ✅ 平均組件大小 < 120 行
- ✅ 使用自定義 Hooks
- ✅ 語法測試通過

---

## 📋 Phase 5: 錯誤處理和日誌 [+2 分]

### 目標
- 統一錯誤處理中間件
- 結構化日誌系統
- 請求追蹤

### 任務清單

#### 5.1 錯誤處理中間件 (1小時)
**優先級**: ⭐⭐

```python
# backend/core/exceptions.py
from fastapi import Request, status
from fastapi.responses import JSONResponse

class AppException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
            "path": request.url.path
        }
    )
```

#### 5.2 結構化日誌 (1小時)
**優先級**: ⭐⭐

```python
# backend/core/logging.py
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

#### 5.3 請求追蹤 (1小時)
**優先級**: ⭐

```python
import uuid

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    logger.info(f"Request {request_id}: {request.method} {request.url.path}")

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
```

**成功標準**:
- ✅ 所有錯誤統一格式返回
- ✅ 日誌記錄關鍵操作
- ✅ 每個請求有唯一 ID

---

## 📋 Phase 6: Docker 部署配置 [+3 分]

### 目標
- Docker 容器化
- docker-compose 一鍵啟動
- 環境變量管理

### 任務清單

#### 6.1 Backend Dockerfile (1小時)
**優先級**: ⭐⭐

```dockerfile
# backend/Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 6.2 Frontend Dockerfile (1小時)
**優先級**: ⭐⭐

```dockerfile
# Dockerfile
FROM node:18-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
```

#### 6.3 docker-compose.yml (1小時)
**優先級**: ⭐⭐

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./turnfix.db
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./backend:/app

  frontend:
    build: .
    ports:
      - "3000:80"
    depends_on:
      - backend
```

#### 6.4 環境變量 (30分鐘)
**優先級**: ⭐⭐

```bash
# .env.example
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./turnfix.db
CORS_ORIGINS=http://localhost:3000
JWT_EXPIRATION=30
```

**成功標準**:
- ✅ `docker-compose up` 一鍵啟動
- ✅ 前後端正常通信
- ✅ 環境變量正確加載

---

## 📋 Phase 7: 完善文檔 [+2 分]

### 任務清單

#### 7.1 API 文檔 (1小時)
**優先級**: ⭐

完善 FastAPI 自動文檔:
- 為所有端點添加詳細描述
- 添加請求/響應範例
- 添加錯誤碼說明

#### 7.2 README.md (1小時)
**優先級**: ⭐⭐

包含:
- 項目簡介
- 功能列表
- 快速開始 (Docker)
- 本地開發設置
- API 文檔鏈接
- 架構圖

#### 7.3 開發者文檔 (1小時)
**優先級**: ⭐

**文件**: `CONTRIBUTING.md`
- 項目架構說明
- 代碼規範
- 提交 PR 流程
- 測試指南

---

## 📋 Phase 8: 最終驗證

### 任務清單

#### 8.1 運行所有測試 (30分鐘)
```bash
# 後端測試
pytest --cov=backend --cov-report=term

# 前端測試
npm run test -- --coverage

# 驗證覆蓋率
# Backend >= 70%
# Frontend >= 60%
```

#### 8.2 代碼質量檢查 (30分鐘)
```bash
# Python
black backend/
isort backend/

# JavaScript
npx prettier --write src/
npx eslint src/
```

#### 8.3 Docker 測試 (30分鐘)
```bash
docker-compose up --build
# 驗證所有服務正常啟動
# 測試 API 端點
```

#### 8.4 最終評分 (30分鐘)
運行評分腳本驗證:
- ✅ Linus 原則: 90+/100
- ✅ 任務完成度: 95+/100
- ✅ 生產就緒: 85+/100
- ✅ 代碼品質: 95+/100

**目標總分: 95/100** ⭐⭐⭐⭐⭐

---

## 🎯 評分預測

| 維度 | 當前 | 完成後 | 提升 |
|------|------|--------|------|
| Linus 原則遵循 (40%) | 36/40 (90%) | 38/40 (95%) | +2 |
| 任務完成度 (30%) | 21/30 (70%) | 28.5/30 (95%) | +7.5 |
| 生產就緒度 (20%) | 6.4/20 (32%) | 17/20 (85%) | +10.6 |
| 代碼品質 (10%) | 9.5/10 (95%) | 9.8/10 (98%) | +0.3 |
| **總分** | **72.9/100** | **93.3/100** | **+20.4** |

**考慮實施品質加分,預計最終: 95-98/100**

---

## 📅 實施時間表

### Day 1 (8小時)
- ✅ Phase 1: 後端測試 (6-8小時)
- ✅ Phase 3.1: JWT 認證 (2.5小時)

### Day 2 (8小時)
- ✅ Phase 2: 前端測試 (4-6小時)
- ✅ Phase 3.2-3.3: 權限和 CORS (2.5小時)
- ✅ Phase 4.1: 重構組件 1 (1.5小時)

### Day 3 (8小時)
- ✅ Phase 4.2: 重構組件 2 (1.5小時)
- ✅ Phase 5: 錯誤處理和日誌 (2-3小時)
- ✅ Phase 6: Docker 配置 (3-4小時)
- ✅ Phase 7: 文檔 (2-3小時)

### Day 4 (4小時)
- ✅ Phase 8: 最終驗證和優化
- ✅ 運行所有測試
- ✅ 修復任何問題
- ✅ 最終評分確認

**總計: 28-32 小時 (3.5-4 天全職工作)**

---

## ✅ 成功標準

達到 95 分需要:

1. **測試覆蓋** ✅
   - 後端 >= 70%
   - 前端 >= 60%
   - 所有測試通過

2. **安全性** ✅
   - JWT 認證正常工作
   - 角色權限正確實施
   - CORS 正確配置

3. **代碼品質** ✅
   - 所有組件 < 150 行
   - 通過 linters
   - 無語法錯誤

4. **部署就緒** ✅
   - Docker 一鍵啟動
   - 環境變量管理
   - 日誌和錯誤處理

5. **文檔完整** ✅
   - README 詳細
   - API 文檔完善
   - 有開發者指南

---

## 🚀 開始執行

準備好了嗎?讓我們開始第一個階段吧!

```bash
# 首先創建測試目錄
mkdir -p backend/tests/{unit,integration}
mkdir -p backend/tests/unit/{repositories,services}
mkdir -p backend/tests/integration/api

# 安裝測試依賴
pip install pytest pytest-cov pytest-asyncio httpx faker
```

讓我知道你準備好了,我們馬上開始!
