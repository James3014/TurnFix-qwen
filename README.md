# TurnFix - 滑雪症狀診斷與練習系統

<div align="center">

**AI 驅動的智能滑雪教練系統**

[![Tests](https://img.shields.io/badge/tests-63%20passing-success)](./backend/tests)
[![Coverage](https://img.shields.io/badge/coverage-73%25-green)](./backend/tests)
[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue)](./LICENSE)

</div>

## 目錄

- [專案簡介](#專案簡介)
- [功能特色](#功能特色)
- [技術架構](#技術架構)
- [快速開始](#快速開始)
  - [使用 Docker (推薦)](#使用-docker-推薦)
  - [本地開發](#本地開發)
- [API 文檔](#api-文檔)
- [測試](#測試)
- [開發指南](#開發指南)
- [專案結構](#專案結構)
- [貢獻指南](#貢獻指南)
- [授權](#授權)

## 專案簡介

TurnFix 是一個創新的滑雪運動輔助系統，專為滑雪愛好者設計。透過 AI 技術，系統能夠:
- 理解滑雪者用自然語言描述的問題
- 識別背後的技術症狀
- 提供個性化的練習建議
- 追蹤進步並調整訓練計劃

### 為什麼選擇 TurnFix?

- **智能理解**: 使用 NLP 技術理解口語化的滑雪問題描述
- **個性化建議**: 根據等級、地形、風格提供定制化練習
- **循證方法**: 基於專業教練經驗和運動科學
- **持續優化**: 透過反饋機制不斷改進推薦質量

## 功能特色

### 核心功能

- **🎯 症狀辨識**: 將口語問題轉換為標準化技術症狀
- **📚 練習建議**: 基於 RAG 技術的個性化練習建議系統
- **💬 自適應追問**: 智能判斷何時需要更多資訊，提供精準追問
- **📊 反饋系統**: 雙層反饋機制（整體推薦質量 + 單卡練習效果）
- **🔐 用戶認證**: JWT-based 安全認證系統
- **👥 角色管理**: 支持普通用戶和管理員角色

### 管理功能

- **📈 分析儀表板**: 完整的使用數據分析和可視化
- **⚙️ 症狀管理**: CRUD 操作管理症狀庫
- **📋 練習卡管理**: 管理和維護練習卡資料庫
- **🔗 映射管理**: 管理症狀與練習卡的關聯關係

### UX 優化

- **⭐ 個人化推薦**: 基於歷史反饋的智能推薦
- **🎥 視頻示範**: 整合視頻教學資源
- **🔊 語音朗讀**: 支持語音播放練習指導
- **📱 響應式設計**: 完美適配各種設備

## 技術架構

### 後端技術棧

- **框架**: FastAPI 0.115
- **語言**: Python 3.11
- **ORM**: SQLAlchemy 2.0
- **資料庫**: PostgreSQL (生產) / SQLite (開發)
- **認證**: JWT (python-jose + passlib)
- **測試**: pytest + pytest-cov (73% 覆蓋率)

### 前端技術棧

- **框架**: React 18 + TypeScript
- **狀態管理**: React Hooks
- **路由**: React Router
- **樣式**: CSS Modules

### AI/ML 組件

- **嵌入模型**: Sentence Transformers
- **向量資料庫**: ChromaDB
- **相似度搜索**: FAISS

### 基礎設施

- **容器化**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **部署**: 支持雲端部署 (Vercel, Railway, etc.)

## 快速開始

### 使用 Docker (推薦)

最簡單的方式是使用 Docker Compose 一鍵啟動所有服務:

```bash
# 1. 克隆專案
git clone https://github.com/yourusername/TurnFix-qwen.git
cd TurnFix-qwen

# 2. 配置環境變量
cp .env.example .env
# 編輯 .env 設置必要的環境變量

# 3. 啟動所有服務
docker-compose up -d

# 4. 訪問應用
# 前端: http://localhost:3000
# 後端 API: http://localhost:8000
# API 文檔: http://localhost:8000/docs
```

### 本地開發

#### 後端設置

```bash
# 1. 進入後端目錄
cd backend

# 2. 創建虛擬環境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安裝依賴
pip install -r requirements.txt

# 4. 設置環境變量
cp ../.env.example .env

# 5. 運行數據庫遷移（如需要）
# python manage.py migrate

# 6. 啟動開發服務器
uvicorn backend.main:app --reload --port 8000
```

#### 前端設置

```bash
# 1. 進入前端目錄
cd frontend

# 2. 安裝依賴
npm install

# 3. 啟動開發服務器
npm start
```

## API 文檔

### 認證端點

```
POST   /api/v1/auth/register     # 用戶註冊
POST   /api/v1/auth/login        # 用戶登錄
GET    /api/v1/auth/me           # 獲取當前用戶信息
GET    /api/v1/auth/verify       # 驗證 token
```

### 核心功能端點

```
POST   /api/v1/ski-tips                    # 獲取滑雪建議
POST   /api/v1/followup-needs              # 獲取追問需求
POST   /api/v1/session-feedback            # 提交會話反饋
POST   /api/v1/practice-card-feedback      # 提交練習卡反饋
```

### 管理端點 (需要管理員權限)

```
GET    /api/v1/admin/symptoms              # 獲取所有症狀
POST   /api/v1/admin/symptoms              # 創建症狀
GET    /api/v1/admin/symptoms/{id}         # 獲取單個症狀
PUT    /api/v1/admin/symptoms/{id}         # 更新症狀
DELETE /api/v1/admin/symptoms/{id}         # 刪除症狀

GET    /api/v1/admin/practice-cards        # 練習卡管理
POST   /api/v1/admin/practice-cards
...
```

**完整 API 文檔**: 啟動服務後訪問 http://localhost:8000/docs

## 測試

### 運行測試

```bash
# 運行所有測試
cd backend
pytest

# 運行測試並查看覆蓋率
pytest --cov=backend --cov-report=term-missing

# 運行特定測試文件
pytest tests/unit/services/test_simple_ski_tips.py

# 運行特定測試類
pytest tests/unit/repositories/test_symptom_repository.py::TestSymptomRepository
```

### 測試覆蓋率

當前測試狀態:
- **總覆蓋率**: 73%
- **測試數量**: 63 個
- **通過率**: 100%

覆蓋範圍:
- ✅ Repository 層: 完整覆蓋
- ✅ Service 層: 高覆蓋率 (90%+)
- ✅ API 端點: 集成測試覆蓋
- ⚠️ 部分服務待補充

## 開發指南

### 代碼風格

遵循 Linus Torvalds 的"好品味"原則:
- 簡單直接，避免過度工程
- 每個函數/組件單一職責
- 組件不超過 150 行
- 清晰的命名和註釋

### 提交規範

```
<type>: <subject>

<body>

<footer>
```

類型 (type):
- feat: 新功能
- fix: 修復 bug
- docs: 文檔更新
- style: 代碼格式調整
- refactor: 重構
- test: 測試相關
- chore: 構建/工具相關

### 分支策略

- `main`: 生產分支
- `develop`: 開發分支
- `feature/*`: 功能分支
- `fix/*`: 修復分支

## 專案結構

```
TurnFix-qwen/
├── backend/                    # 後端代碼
│   ├── api/                   # API 路由
│   │   └── v1/               # API v1 端點
│   ├── core/                 # 核心配置
│   ├── database/             # 資料庫配置和倉儲
│   ├── models/               # 資料模型
│   ├── services/             # 業務邏輯
│   ├── tests/                # 測試文件
│   │   ├── unit/            # 單元測試
│   │   └── integration/     # 集成測試
│   ├── Dockerfile            # Docker 配置
│   └── requirements.txt      # Python 依賴
├── frontend/                  # 前端代碼
│   ├── src/
│   │   ├── components/      # React 組件
│   │   ├── hooks/           # 自定義 Hooks
│   │   └── services/        # API 服務
│   └── package.json         # Node 依賴
├── docker-compose.yml         # Docker Compose 配置
├── .env.example              # 環境變量範例
├── ROADMAP_TO_95.md          # 開發路線圖
└── README.md                 # 本文檔
```

## 環境變量

必需的環境變量:

```bash
# 後端
DATABASE_URL=postgresql://user:pass@localhost:5432/turnfix
SECRET_KEY=your-secret-key-here

# 可選
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-supabase-key
YOUTUBE_API_KEY=your-youtube-key
DEBUG=False
```

## 貢獻指南

我們歡迎任何形式的貢獻！

1. Fork 本專案
2. 創建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的改動 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟一個 Pull Request

### 開發檢查清單

在提交 PR 前，請確保:

- [ ] 所有測試通過 (`pytest`)
- [ ] 代碼覆蓋率不降低
- [ ] 遵循代碼風格規範
- [ ] 更新相關文檔
- [ ] 添加必要的測試

## 路線圖

查看 [ROADMAP_TO_95.md](./ROADMAP_TO_95.md) 了解專案發展計劃。

## 授權

本專案採用 MIT 授權。詳見 [LICENSE](./LICENSE) 文件。

## 聯繫方式

- 專案維護者: Your Name
- Email: your.email@example.com
- 問題反饋: [GitHub Issues](https://github.com/yourusername/TurnFix-qwen/issues)

---

<div align="center">

**用 ❤️ 和 ⛷️ 打造**

[報告 Bug](https://github.com/yourusername/TurnFix-qwen/issues) · [請求功能](https://github.com/yourusername/TurnFix-qwen/issues) · [貢獻代碼](https://github.com/yourusername/TurnFix-qwen/pulls)

</div>
