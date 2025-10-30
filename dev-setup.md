# TurnFix 開發環境設定指南

## 1. 技術架構概覽

TurnFix 採用輕量化方案實現 MVP，但架構設計考慮未來擴展：
- **後端框架**：Python + FastAPI
- **前端框架**：React + TypeScript
- **資料庫**：SQLite
- **向量資料庫**：ChromaDB
- **AI/LLM**：Sentence Transformers + Hugging Face Models

## 2. 開發環境需求

### 2.1 系統需求
- Python 3.9+
- Node.js 16+
- npm 或 yarn
- Git

### 2.2 Python 套件需求 (requirements.txt)
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
sqlite3  # 內建於 Python
chromadb==0.4.21
sentence-transformers==2.2.2
pydantic==2.5.0
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx==0.25.0
alembic==1.13.1
python-multipart==0.0.6
```

### 2.3 測試工具
- **pytest**：主要測試框架
- **pytest-asyncio**：用於非同步測試
- **pytest-cov**：代碼覆蓋率分析
- **httpx**：API 整合測試

### 2.3 Node.js 套件需求 (package.json)
```json
{
  "name": "turnfix-frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "@types/react": "^18.2.37",
    "@types/react-dom": "^18.2.15",
    "typescript": "^4.9.5",
    "axios": "^1.6.0",
    "react-router-dom": "^6.18.0"
  }
}
```

## 3. 資料庫設計

使用 SQLAlchemy ORM 實現，並採用六邊形架構（端口與適配器模式）。

### 3.1 資料庫遷移
使用 Alembic 管理資料庫 schema 變更，便於未來遷移到其他資料庫。

## 4. AI/LLM 設計

### 4.1 RAG 架構
1. 知識來源：影片逐字稿（統一來源）
2. 預處理：清洗、分段、結構化、向量化
3. 儲存：ChromaDB 向量資料庫
4. 檢索：根據使用者問題檢索相關知識片段
5. 選擇：根據檢索結果和使用者條件選擇最適合的練習卡

### 4.2 資料處理流程
1. **自動化提取**：
   - 從影片逐字稿自動分離症狀描述與練習建議
   - 建立結構化資料格式
   - 標記適用條件（等級、地形、風格）

2. **知識庫維護**：
   - 自動化流程處理新來源
   - 定期重新向量化和索引
   - 版本控制與回滾能力

3. **品質控制**：
   - 人工審核機制
   - 使用者回饋整合
   - 定期審查知識準確性

### 4.2 模型選擇
- **嵌入模型**：Sentence Transformers (paraphrase-multilingual-MiniLM-L12-v2)
    - 支援多語言，包括中文
    - 適用於語義相似度匹配
    - 輕量級，適合 Serverless 環境
- **生成模型**：Hugging Face 開源模型（根據需要選擇）

### 4.3 AI 模型效能優化
1. **模型量化**：
   - 使用 int8 量化減少模型大小和推理時間
   - 在準確性和效能間取得平衡

2. **模型快取**：
   - 在應用程式啟動時載入模型到記憶體
   - 避免重複載入造成的延遲

3. **預計算向量**：
   - 對常見症狀和練習卡預計算向量表示
   - 加速檢索過程

4. **同義詞庫優化**：
   - 建立精確的同義詞映射
   - 減少對 AI 模型的依賴，提高回應速度

## 5. 安全性措施

1. **輸入驗證與清理**
   - 使用 Pydantic 進行資料驗證
   - 實施資料格式驗證和範圍檢查
   - 過濾惡意輸入
   - 防範提示詞注入攻擊

2. **防止 SQL 注入和 XSS 攻擊**
   - 使用 SQLAlchemy ORM 避免直接 SQL 查詢
   - 使用參數化查詢
   - 實施內容清理機制

3. **API 速率限制與金鑰管理**
   - 使用 FastAPI 的內建速率限制功能
   - 基於 IP 或 API 金鑰的速率限制
   - 實施 API 金鑰管理和輪換
   - 保護 AI 模型免受濫用

4. **使用者隱私保護**
   - 避免在日誌中記錄敏感資料
   - 實施資料加密 (TLS/SSL)
   - 遵循資料保護法規

5. **AI 模型安全**
   - 防範提示詞注入攻擊
   - 實施內容過濾機制
   - 防止模型濫用
   - 建立模型使用監控

## 6. 錯誤處理與彈性設計

1. **錯誤恢復機制**
   - 實施熔斷器模式，防止級聯故障
   - 使用重試邏輯處理外部服務呼叫
   - 實施指數退避策略

2. **降級策略**
   - 無法識別症狀時提供「最安全基礎練習組」
   - AI 服務不可用時使用規則基礎的備用方案
   - 預設練習卡映射作為備用

3. **監控與告警**
   - API 響應時間監控
   - 錯誤率追蹤
   - 資源使用率監控
   - 高錯誤率和異常響應時間告警

## 7. 使用者體驗優化

1. **介面設計**
   - 實施回應式設計，適應不同裝置尺寸
   - 優化觸控介面，考慮行動裝置使用場景
   - 提供智慧提示與自動完成功能

2. **效能優化**
   - 實施資料預載與快取機制
   - 非同步處理長時間操作
   - 優化 API 響應時間以符合 P95 < 2.5s 目標

3. **易用性改進**
   - 提供首次使用導覽
   - 清晰的錯誤訊息和進度指示器
   - 簡化選填資訊流程，提供預設選項

## 8. 分析與回饋系統

1. **使用者行為分析**
   - 追蹤使用者輸入的症狀描述
   - 分析選擇的練習卡類型
   - 追蹤使用者評價（👍/👎）和回饋

2. **系統效能監控**
   - API 響應時間監控
   - 系統可用性指標
   - 資源使用率追蹤

3. **回饋收集與分析**
   - 收集自由文字回饋
   - 分析回饋內容以改進系統
   - 追蹤回饋處理狀態

## 9. 維護與營運

1. **CI/CD 流程**
   - 自動化測試與部署
   - 版本控制和發布管理
   - 回滾機制

2. **系統維護**
   - 定期更新依賴套件
   - 系統安全更新
   - 效能調優

3. **回歸測試**
   - 核心功能回歸測試
   - AI 模型準確性驗證
   - 效能基準測試

## 10. 擴展準備

### 6.1 資料庫遷移
當需要更高性能時，可從 SQLite 遷移至 PostgreSQL：
- SQLAlchemy ORM 抽象化了資料庫操作
- Alembic 提供資料庫 schema 遷移工具
- 預設使用相容的 SQL 語法

### 6.2 向量資料庫
當需要更強大的向量搜尋功能時，可從 ChromaDB 遷移至：
- Weaviate
- Pinecone
- 或其他專業向量資料庫

### 6.3 後端擴展
當需要更複雜的架構時，可將單體應用拆分為：
- 微服務架構
- 使用消息隊列處理非同步任務
- 加入快取層（如 Redis）

### 6.4 前端擴展
根據需求可加入：
- 服務端渲染 (SSR)
- 靜態產生 (SSG)
- 更複雜的狀態管理 (Redux)

## 7. 開發流程

### 7.1 後端開發
1. 定義領域模型和服務介面
2. 實作資料庫抽象層
3. 實作業務邏輯
4. 建立 API 端點
5. 撰寫測試（採用混合方法）

### 7.2 前端開發
1. 設計 UI 組件
2. 建立 API 串接工具
3. 實作頁面邏輯
4. 整合狀態管理
5. 撰寫測試（採用混合方法）

### 7.3 測試策略
- **核心邏輯 TDD**：為核心業務邏輯先寫測試再開發
- **單元測試**：測試獨立功能和服務
- **整合測試**：測試組件間的協作
- **端到端測試**：測試完整使用者流程
- **AI 模型測試**：建立準確性基準後定期執行
- **效能測試**：系統開發後執行
- **安全測試**：定期執行安全相關測試

## 8. 部署準備

### 8.1 Docker 配置
提供 Dockerfile 和 docker-compose.yml 檔案，便於容器化部署。

### 8.2 環境變數
設定必要的環境變數以支援不同部署環境：

```
# 資料庫設定
DATABASE_URL=sqlite:///./turnfix.db
DATABASE_ENGINE=sqlite

# AI 模型設定
EMBEDDING_MODEL=all-MiniLM-L6-v2
AI_PROVIDER=huggingface

# 向量資料庫設定
VECTOR_DB_TYPE=chroma
VECTOR_DB_PATH=./vector_store

# 安全設定
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 9. 部署配置

### 9.1 Serverless 部署 (Vercel)
1. 前端部署到 Vercel：
   - 連接 GitHub 倉庫
   - 設定 build command: `npm run build`
   - 設定 output directory: `build`

2. 後端 API 部署到 Vercel Functions：
   - 設定 Python runtime
   - 配置環境變數
   - 設定 API 路由

### 9.2 資料庫 (Supabase)
1. 建立 Supabase 專案
2. 配置資料庫 schema
3. 設定 API keys 和權限
4. 配置 real-time 功能（如需要）

### 9.3 環境變數配置
```
# Vercel 部署環境變數
NEXT_PUBLIC_API_URL=your-vercel-url
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-supabase-anon-key

# AI 模型設定
EMBEDDING_MODEL=all-MiniLM-L6-v2
AI_PROVIDER=huggingface

# 向量資料庫設定
VECTOR_DB_TYPE=chroma
VECTOR_DB_PATH=./vector_store
```

## 10. 監控與維護

- API 回應時間目標：P95 < 2.5s
- 使用 Vercel Analytics 監控效能
- 設定錯誤追蹤機制 (如 Sentry)
- 建立健康檢查端點
- 定期檢查 Supabase 資料庫效能