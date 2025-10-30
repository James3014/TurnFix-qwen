# API Doc Generator Skill

## 🎯 名稱
api-doc-generator

## 📝 描述
根據 TurnFix 的 API 規格文檔（ADMIN_FEEDBACK_ANALYTICS_DESIGN.md、STAR_RATING_FEEDBACK_DESIGN.md 等），自動生成標準化的 API 文檔。支持生成 OpenAPI 3.0 規格、Postman Collection、API 文檔 HTML 和 API 摘要表。

## 🎨 功能

### OpenAPI 3.0 規格生成
- ✅ 完整的 OpenAPI 3.0 YAML/JSON 規格
- ✅ 所有 API 端點定義（GET, POST, PUT, DELETE）
- ✅ 請求/響應 Schema 定義
- ✅ 參數定義（path, query, body）
- ✅ HTTP 狀態碼和錯誤響應
- ✅ 安全定義（Authentication）
- ✅ 支持 Swagger UI 和 Redoc

### Postman Collection 生成
- ✅ 完整的 Postman 集合文件
- ✅ 預設的請求示例
- ✅ 環境變量配置（base_url, auth_token）
- ✅ 測試腳本（自動驗證響應）
- ✅ Pre-request 腳本（準備數據）

### API 文檔 HTML 生成
- ✅ 美觀的 HTML API 文檔
- ✅ 交互式端點瀏覽
- ✅ 實時代碼示例
- ✅ 請求/響應範例
- ✅ 搜索和過濾功能

### 快速參考表
- ✅ API 端點速查表（Markdown）
- ✅ 參數對照表
- ✅ 常見錯誤代碼表
- ✅ 速率限制和配額說明

## 💻 使用方式

### 基本用法

```
"根據 ADMIN_FEEDBACK_ANALYTICS_DESIGN.md 生成 API-207 的 OpenAPI 規格"
```

### 進階用法

```
"為反饋系統（API-204 和 API-207）生成完整的 OpenAPI 3.0 規格和 Postman Collection"

"根據 STAR_RATING_FEEDBACK_DESIGN.md 生成 API-204 的 Postman 集合，包括測試腳本"

"生成所有 API 端點的 HTML 文檔（包括認證、速率限制、錯誤處理）"

"為 TurnFix 生成完整的 API 文檔包，包括 OpenAPI、Postman、HTML 和速查表"

"根據 tasks.md 中的 API 任務生成缺失的 API 文檔"
```

## 📋 輸出格式

### OpenAPI 3.0 規格
```yaml
openapi: 3.0.0
info:
  title: TurnFix Feedback API
  version: 1.0.0
paths:
  /api/v1/feedback/practice-card:
    post:
      summary: Submit practice card feedback
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PracticeCardFeedback'
      responses:
        '201':
          description: Feedback created successfully
```

### Postman Collection
```json
{
  "info": {
    "name": "TurnFix Feedback API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Submit Star Rating",
      "request": {
        "method": "POST",
        "url": "{{base_url}}/api/v1/feedback/practice-card"
      }
    }
  ]
}
```

### API 文檔 HTML
```html
<!-- 美觀的交互式 API 文檔 -->
<!-- 包括實時試用功能 -->
<!-- 代碼示例和響應範例 -->
```

## 📚 支持的源文檔

| 源文檔 | API 覆蓋 | 優先級 |
|--------|---------|--------|
| ADMIN_FEEDBACK_ANALYTICS_DESIGN.md | API-207 (6 個端點) | P1 |
| STAR_RATING_FEEDBACK_DESIGN.md | API-204 (3 個端點) | P1 |
| sdd-TurnFix.md | 整體架構和認證 | P2 |
| tasks.md | 所有 API-2xx 任務 | P2 |

## 🎯 生成時的最佳實踐

✅ **必須遵循**：
- 完整的 Schema 定義（所有字段和類型）
- 真實的示例數據（應該匹配實現）
- 完整的錯誤代碼文檔（包括錯誤訊息）
- 安全和認證說明
- API 版本號和變更歷史

❌ **應避免**：
- 不完整的 Schema 定義
- 虛假的示例數據
- 缺失錯誤情況
- 不更新文檔（應與代碼同步）

## 🔗 相關參考文件

- **ADMIN_FEEDBACK_ANALYTICS_DESIGN.md** - API-207 詳細規格
- **STAR_RATING_FEEDBACK_DESIGN.md** - API-204 詳細規格
- **tasks.md** - 所有 API 任務定義
- **STAR_RATING_QUICK_REFERENCE.md** - API 速查表
- **architecture.md** - 系統架構和認證方式

## 🚀 工作流程整合

1. **開發前**：生成 OpenAPI 規格和 Postman Collection
2. **開發中**：用 Postman 手動測試 API
3. **開發完成**：更新 OpenAPI 規格和 HTML 文檔
4. **發布前**：驗證文檔與實現一致

## 🔑 生成內容清單

### OpenAPI 規格應包括
- [ ] 所有端點定義（GET, POST, PUT, DELETE）
- [ ] 完整的請求 Schema
- [ ] 完整的響應 Schema
- [ ] 所有可能的 HTTP 狀態碼
- [ ] 認證方式（JWT, OAuth 等）
- [ ] 速率限制和配額
- [ ] 端點標籤和分組

### Postman Collection 應包括
- [ ] 所有端點的請求
- [ ] 預設的環境變量
- [ ] 示例請求數據
- [ ] Pre-request 腳本（如需要）
- [ ] 測試腳本（驗證響應）
- [ ] 資料夾組織

### HTML 文檔應包括
- [ ] 清晰的端點分組
- [ ] 實時試用功能
- [ ] 代碼示例（多種語言）
- [ ] 響應示例
- [ ] 搜索和過濾
- [ ] 深色/淺色主題支持

## 💡 範例請求

```
"根據 ADMIN_FEEDBACK_ANALYTICS_DESIGN.md 生成完整的 API-207 文檔包，包括：
1. OpenAPI 3.0 規格（可用於 Swagger UI）
2. Postman Collection（包括測試腳本）
3. HTML 文檔（用於開發者查閱）
4. API 快速參考表（Markdown）

確保包含所有 6 個端點的詳細定義和示例"
```

## 📊 支持的 API 類型

| API 類型 | 特殊處理 |
|---------|---------|
| RESTful | 完全支持 |
| GraphQL | 需要額外配置 |
| 分頁 API | 自動包含分頁參數 |
| 批量操作 | 支持批量端點 |
| WebSocket | 不支持（計劃中） |

## 🛠️ 生成工具集

- **OpenAPI Generator** - 從規格生成代碼
- **Swagger UI** - 交互式 API 文檔
- **Redoc** - 美觀的 API 文檔
- **Postman CLI** - 命令行集合管理
- **dredd** - API 合規性測試

## 🔄 版本管理

- ✅ 追蹤 API 版本歷史
- ✅ 標記破壞性變更
- ✅ 提供遷移指南
- ✅ 維護向後兼容性列表

## 🎓 推薦工作流

```
1. 設計階段：根據設計文檔生成 OpenAPI 規格
   └─ 用於 API 設計審批

2. 開發前：生成 Postman Collection
   └─ 前端/移動端可以立即開始開發（Mock API）

3. 開發中：使用 Postman 測試 API
   └─ 團隊協作和手動測試

4. 開發完成：更新 OpenAPI 規格
   └─ 同步最新的實現細節

5. 發布：生成 HTML 文檔
   └─ 開發者使用文檔

6. 維護：定期同步文檔與代碼
   └─ 確保文檔不過時
```

---

**版本**：v1.0
**維護者**：TurnFix 開發團隊
**更新日期**：2025-10-28
