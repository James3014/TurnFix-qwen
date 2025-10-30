# TurnFix 自定義 Skills 指南

**版本**：v1.0
**更新日期**：2025-10-28
**狀態**：✅ 已安裝，可立即使用

---

## 🎯 已安裝的 Skills

### 1️⃣ **test-generator** - 測試代碼生成

**位置**：`.claude/skills/test-generator/`

**功能**：
- 🧪 根據 API 規格自動生成 pytest 測試代碼
- 🎨 根據 UI 設計自動生成 Jest 測試代碼
- 📋 生成完整的測試套件（含邊界情況、異常處理）
- ✅ 遵循 TDD 規範和 Given-When-Then 模式

**快速使用**：
```
"為 API-204.3 生成 pytest 測試代碼"

"為 UI-307.2 星數評分組件生成 Jest 測試"

"根據 TEST-406 生成管理後台的完整測試套件"
```

---

### 2️⃣ **api-doc-generator** - API 文檔生成

**位置**：`.claude/skills/api-doc-generator/`

**功能**：
- 📚 生成 OpenAPI 3.0 規格（可用於 Swagger UI）
- 📮 生成 Postman Collection（含測試腳本）
- 🌐 生成美觀的 HTML API 文檔
- ⚡ 生成 API 速查表

**快速使用**：
```
"根據 ADMIN_FEEDBACK_ANALYTICS_DESIGN.md 生成 API-207 的 OpenAPI 規格"

"為反饋系統生成完整的 Postman Collection，包括測試腳本"

"生成所有 API 端點的 HTML 文檔"
```

---

## 🚀 如何使用

### 方式 1：直接請求（推薦）

```
我: "為 API-207.1 反饋統計端點生成 pytest 測試代碼，
     包括層一和層二統計的驗證測試"

Claude 會自動使用 test-generator Skill 生成代碼
```

### 方式 2：指定特定 Skill

```
我: "使用 test-generator Skill，為 API-204.3 生成測試代碼"

Claude 會使用該 Skill 生成代碼
```

### 方式 3：組合多個 Skills

```
我: "首先用 api-doc-generator 生成 API-207 的 OpenAPI 規格，
     然後用 test-generator 根據規格生成測試代碼"

Claude 會按順序使用兩個 Skills
```

---

## 💡 常見使用場景

### 場景 1：開發新 API 端點

```bash
# 步驟 1：生成 API 文檔
我: "用 api-doc-generator 為 API-207.5（篩選和導出）生成 OpenAPI 規格"
→ 獲得完整的 API 文檔

# 步驟 2：生成測試代碼
我: "用 test-generator 根據 API-207.5 的規格生成 pytest 測試"
→ 獲得完整的測試代碼

# 步驟 3：開始開發
實現 API 端點，確保測試通過
```

### 場景 2：開發新 UI 組件

```bash
# 步驟 1：生成 UI 測試
我: "用 test-generator 為 UI-308.6 儀表板組件生成 Jest 測試"
→ 獲得組件測試代碼

# 步驟 2：開始開發
實現組件，確保所有測試通過
```

### 場景 3：生成完整文檔包

```bash
# 一次性生成所有 API 文檔
我: "用 api-doc-generator 為整個反饋系統（API-204 和 API-207）
     生成完整的文檔包：
     1. OpenAPI 規格
     2. Postman Collection
     3. HTML 文檔
     4. 快速參考表"
→ 獲得所有文檔
```

---

## 🎯 推薦用法順序

### 第 1 周（核心反饋系統）
```
1. api-doc-generator → API-204.3-5 文檔
2. test-generator → API-204.3-5 測試
3. api-doc-generator → API-207.1-2 文檔
4. test-generator → API-207.1-2 測試
```

### 第 2 周（管理後台）
```
1. api-doc-generator → API-207.3-4 文檔
2. test-generator → API-207.3-4 測試
3. test-generator → UI-308.6-8 測試
```

### 第 3 周（導出和優化）
```
1. api-doc-generator → API-207.5-6 文檔
2. test-generator → API-207.5-6 測試
3. test-generator → UXP-18xx 功能測試
```

---

## 📋 輸出物檢查清單

### 用 api-doc-generator 生成時確認

- [ ] OpenAPI 規格包含所有端點
- [ ] 所有請求 Schema 完整
- [ ] 所有響應 Schema 定義
- [ ] HTTP 狀態碼覆蓋（200, 201, 400, 401, 500 等）
- [ ] 認證方式說明
- [ ] 速率限制說明
- [ ] Postman Collection 包含示例請求
- [ ] 預設環境變量配置正確

### 用 test-generator 生成時確認

- [ ] 測試名稱清晰（`test_should_*` 模式）
- [ ] 遵循 Given-When-Then 結構
- [ ] 包含邊界情況測試
- [ ] Mock 外部依賴（數據庫、API）
- [ ] 異常情況測試
- [ ] 測試覆蓋率預估 ≥ 80%
- [ ] 包含詳細的測試註釋

---

## 🔧 自定義和擴展

### 修改 Skill 定義

如果需要修改 Skill 的行為，編輯相應的 SKILL.md：

```bash
# 編輯 test-generator Skill
vim .claude/skills/test-generator/SKILL.md

# 編輯 api-doc-generator Skill
vim .claude/skills/api-doc-generator/SKILL.md
```

### 添加更多 Skill（未來）

P2 優先級 Skills（待創建）：
```
- coverage-analyzer - 分析測試覆蓋率
- task-tracker - 追蹤開發進度
- code-reviewer - 自動代碼審查
```

---

## 🐛 故障排除

### 問題 1：Skill 沒有被自動激活

**症狀**：請求與 Skill 相關但沒有被使用

**解決**：
```
更明確的描述你的需求，例如：
❌ 差："幫我生成測試"
✅ 好："用 test-generator Skill 為 API-204.3 生成 pytest 測試代碼"
```

### 問題 2：生成的代碼不符合需求

**症狀**：生成的測試或文檔不是想要的格式

**解決**：
```
在請求中提供更多細節：
"用 test-generator 為 API-207.1 生成 pytest 測試，
 要求：
 1. 使用 conftest.py 中定義的 Fixtures
 2. 包括時間相關的趨勢測試
 3. 驗證相關性係數計算
 4. 覆蓋率 ≥ 90%"
```

### 問題 3：生成的 API 文檔與實現不符

**症狀**：文檔中的 API 規格與實現不一致

**解決**：
```
重新生成文檔，並提供最新的設計文件：
"基於最新的 ADMIN_FEEDBACK_ANALYTICS_DESIGN.md，
 重新生成 API-207 的 OpenAPI 規格"
```

---

## 📊 使用統計和建議

### 預期使用頻率

| Skill | 頻率 | 何時使用 |
|-------|------|---------|
| test-generator | 高 | 每個功能開發前 |
| api-doc-generator | 中 | API 開發前和完成時 |

### 預期時間節省

| 任務 | 手動 | 用 Skill | 節省時間 |
|------|------|---------|---------|
| 生成 API 測試 | 2h | 10min | 90% |
| 生成 API 文檔 | 3h | 15min | 91% |
| 生成 UI 測試 | 1.5h | 10min | 89% |

---

## 🎓 最佳實踐

### 1. always 先生成文檔再生成測試
```
✅ 好：先生成 API 文檔，再根據文檔生成測試
❌ 不好：直接生成測試，沒有清晰的 API 規格
```

### 2. 提供充足的上下文
```
✅ 好："根據 ADMIN_FEEDBACK_ANALYTICS_DESIGN.md
        Section 🔌 API 設計詳解 生成..."
❌ 不好："生成 API 測試"
```

### 3. 審查生成的代碼
```
✅ 生成後檢查：
  - 代碼風格是否一致
  - 邏輯是否正確
  - 是否遵循了最佳實踐
  - 測試覆蓋率是否足夠
```

### 4. 反覆迭代改進
```
如果第一次生成不滿意：
"修改上面生成的測試，添加以下內容：
 - 並發請求的測試
 - 大數據集的性能測試
 - 邊界情況的驗證"
```

---

## 📞 常見問題

| 問題 | 答案 |
|------|------|
| 可以同時使用兩個 Skill 嗎？ | 可以，可以在一個請求中組合 |
| Skill 生成的代碼可以直接用嗎？ | 大部分可以，但建議審查後再用 |
| 可以修改 Skill 的定義嗎？ | 可以，編輯 SKILL.md 文件 |
| 如何創建新的 Skill？ | 在 `.claude/skills/` 下創建新目錄和 SKILL.md |

---

## 🚀 下一步

### 立即試用

```bash
# 試試 test-generator
"為 API-204.3 星數回饋生成 pytest 測試代碼"

# 試試 api-doc-generator
"根據 STAR_RATING_FEEDBACK_DESIGN.md 生成 API-204 的 OpenAPI 規格"
```

### 計劃加入（P2 優先級）

```
- coverage-analyzer：分析和改進測試覆蓋率
- task-tracker：自動追蹤開發進度
- code-reviewer：自動代碼質量檢查
```

---

**祝你開發順利！🚀**

如果有任何問題或建議，在提交 PR 時提到相關 Skill 即可。

