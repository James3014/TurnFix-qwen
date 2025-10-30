# TurnFix - 滑雪症狀診斷與練習系統

TurnFix 是一個 AI 驅動的滑雪運動輔助系統，專為滑雪愛好者設計，幫助他們識別滑行問題並提供個性化練習建議。

## 功能特色

- **症狀辨識**: 將口語問題轉換為標準化症狀
- **練習建議**: 基於 RAG 技術的個性化練習建議
- **自適應追問**: 智能追問以獲得更多資訊
- **反饋系統**: 雙層反饋機制（整體推薦 + 練習卡質量）
- **管理後台**: 完整的分析儀表板
- **UX 優化**: 個人化推薦、視頻示範、語音朗讀等

## 技術架構

- **前端**: React + TypeScript
- **後端**: Python + FastAPI
- **資料庫**: SQLite (開發階段) / Supabase (部署階段)
- **AI 模型**: Sentence Transformers
- **向量資料庫**: ChromaDB

## 安裝與使用

### 後端設置

1. 安裝依賴:
   ```bash
   pip install -r requirements.txt
   ```

2. 設置環境變數:
   ```bash
   cp .env.example .env
   # 編輯 .env 文件配置環境變數
   ```

3. 啟動服務:
   ```bash
   cd backend
   uvicorn main:app --reload --port 8000
   ```

### 前端設置

1. 安裝依賴:
   ```bash
   cd frontend
   npm install
   ```

2. 啟動服務:
   ```bash
   npm start
   ```

## 資料處理工具

TurnFix 包含完整的資料處理工具鏈:

- **資料清洗**: `python tools/data_preparation/cli.py clean`
- **知識抽取**: `python tools/data_preparation/cli.py extract`
- **品質驗證**: `python tools/data_preparation/cli.py validate`
- **知識導入**: `python tools/data_preparation/cli.py import`

## API 文檔

核心 API 端點:
- `/ski-tips`: 獲取滑雪技巧建議
- `/followup-needs`: 獲取自適應追問
- `/session-feedback`: 提交會話反饋
- `/practice-card-feedback`: 提交練習卡反饋
- `/admin/*`: 管理後台端點

## 授權

此專案以 MIT 授權。