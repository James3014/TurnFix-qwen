# TurnFix 資料清洗工具 - 使用指南

## 快速開始

資料清洗工具是一個**獨立於 TurnFix 應用的輔助工具集**，用於將您的影片逐字稿和教練答覆轉化為結構化知識，供 RAG 系統使用。

### 工具位置
```
TurnFix/
├── tools/
│   └── data_preparation/
│       ├── cli.py              # 主入口
│       ├── scripts/
│       │   ├── clean_transcripts.py
│       │   ├── extract_knowledge.py
│       │   ├── validate_data.py
│       │   └── import_to_chroma.py
│       ├── data_in/            # 放入原始逐字稿
│       ├── data_out/           # 清洗後的結果
│       └── README.md
```

---

## 工具工作流程

### 階段 1：清洗（Clean）
**輸入**：.txt 或 .md 格式的逐字稿
**輸出**：`cleaned_*.json` - 清洗後的結構化文本

```bash
python cli.py clean --input ./data_in --output ./data_out
```

**做什麼**：
- 移除逐字稿中的雜訊（多餘空格、特殊符號、重複內容）
- 正規化格式（統一標點符號、大小寫）
- 檢測語言（中文/英文/混合）
- 按段落或句子分割（保留上下文用於知識抽取）

### 階段 2：抽取（Extract）
**輸入**：`cleaned_*.json`
**輸出**：`candidates_*.json` - 自動抽取的知識片段，**標記為待審核**

```bash
python cli.py extract --input ./data_out --review-mode
```

**做什麼**：
- 自動識別症狀詞彙（「後坐」「重心」等）及其上下文
- 識別練習建議的結構（動作要點、常見錯誤、建議次數）
- 生成候選知識片段（JSON 格式）
- 標記每個片段的置信度（低/中/高）

**輸出格式範例**：
```json
{
  "id": "symptom_001",
  "symptom": "轉彎會後坐",
  "symptom_normalized": "後坐",
  "practice_tips": [
    "保持膝蓋彎曲",
    "外腳施力 70-80%",
    "中立後再換刃"
  ],
  "pitfalls": "避免提前壓內腳",
  "dosage": "藍線 6 次/趟 × 3 趟",
  "source_snippet": "...(原文摘錄)...",
  "source_file": "transcript_001.txt",
  "confidence": "high",
  "needs_review": true
}
```

### 階段 3：驗證（Validate）
**輸入**：`candidates_*.json`
**輸出**：`validation_report.txt` - 品質檢查報告

```bash
python cli.py validate --input ./data_out
```

**做什麼**：
- 檢查症狀名稱的唯一性（避免重複）
- 驗證練習建議的完整性（是否包含必要字段）
- 檢查文字長度和品質
- 標記異常記錄（缺少字段、過短、置信度低）

**報告輸出範例**：
```
=== 驗證報告 ===
總件數：45
✓ 通過：42 件
⚠ 警告：2 件（建議修改）
✗ 失敗：1 件（需要手動介入）

警告項目：
- symptom_012: 缺少 pitfalls 字段
- symptom_034: dosage 過於簡短，建議補充

失敗項目：
- symptom_008: 置信度 low，建議人工確認或刪除
```

### 階段 4a：人工審核（Local Web UI）
**輸入**：`candidates_*.json`
**輸出**：`approved_*.json` - 人工確認的知識片段

```bash
python cli.py extract --input ./data_out --review-mode
# 自動打開 Web UI: http://localhost:8000
```

**做什麼**（Web UI）：
- 逐個展示待審核的知識片段
- 允許您修改症狀名稱、練習建議、建議次數等
- 支援批量操作（批准/拒絕/標記為需修改）
- 顯示置信度和來源片段供您參考

**Web UI 操作**：
1. 左側列表：待審核項目列表
2. 中央編輯區：修改症狀、練習、建議等
3. 右側：原始文本和置信度信息
4. 底部：批准/拒絕/修改 按鈕
5. 導出：完成審核後，點擊「導出已批准項目」

### 階段 4b：應用內審核（可選）
如果您更傾向在應用的管理後台進行審核：

**在 TurnFix 應用管理後台**：
1. 進入「知識庫管理」→ 「待審核項目」
2. 上傳 `candidates_*.json`
3. 在應用中逐個審核和修改
4. 批准後，應用會自動調用工具進行導入

### 階段 5：導入（Import）
**輸入**：`approved_*.json`
**輸出**：知識已導入 ChromaDB，可被應用使用

```bash
python cli.py import --input ./data_out --chroma-db-path ../backend/chroma_db
```

**做什麼**：
- 將審核後的知識片段轉換為向量格式（使用 Sentence Transformers）
- 批量導入到 ChromaDB（應用的向量資料庫）
- 附加 metadata（來源、更新時間、片段 ID）
- 驗證導入是否成功（檢查向量化和檢索功能）
- 生成導入報告

**導入報告範例**：
```
=== 導入報告 ===
開始時間：2025-10-28 14:00:00
輸入檔案：approved_candidates_001.json
總件數：42

向量化：✓ 42/42
導入 ChromaDB：✓ 42/42
耗時：3.2 秒

完成！知識已可在應用中使用。
```

---

## 完整使用流程

### 初次設定（一次性）

```bash
# 1. 將原始逐字稿放入 data_in/
# 假設您有以下檔案：
#   - transcript_001.txt  (教練答覆)
#   - video_001_transcript.md  (影片逐字稿)

# 2. 執行清洗
cd tools/data_preparation
python cli.py clean --input ./data_in --output ./data_out

# 3. 執行抽取（自動啟動審核 UI）
python cli.py extract --input ./data_out --review-mode
# 在 http://localhost:8000 進行人工審核
# 審核完成後，Web UI 會導出 approved_*.json

# 4. 驗證（可選）
python cli.py validate --input ./data_out

# 5. 導入到應用
python cli.py import --input ./data_out --chroma-db-path ../../backend/chroma_db

# 完成！您的知識庫現在可以被 TurnFix 應用使用
```

### 定期更新（每當有新逐字稿）

```bash
# 1. 將新的逐字稿放入 data_in/
# 2. 運行完整流程或簡化流程

# 簡化流程（推薦自動化）
python cli.py clean --input ./data_in --output ./data_out
python cli.py extract --input ./data_out  # 跳過審核 (--review-mode)，或使用應用內審核
python cli.py import --input ./data_out --chroma-db-path ../../backend/chroma_db
```

### 應用內知識庫管理（可選）

如果您希望在 TurnFix 應用的管理後台進行審核：

```bash
# 1. 清洗和抽取（前兩步一樣）
python cli.py clean --input ./data_in --output ./data_out
python cli.py extract --input ./data_out

# 2. 在 TurnFix 應用管理後台進行審核
# → 進入「知識庫管理」
# → 「上傳待審核項目」
# → 選擇 candidates_*.json
# → 在應用中逐個審核和修改
# → 點擊「批准」，應用會自動呼叫導入工具

# 3. 確認導入完成
# 應用會顯示導入成功訊息
```

---

## 常見情況

### 情況 1：想改動某個已審核的知識片段
```bash
# 1. 修改 approved_*.json 中對應的項目
# 2. 重新導入
python cli.py import --input ./data_out --chroma-db-path ../../backend/chroma_db
```

### 情況 2：發現抽取有誤，需要重新開始
```bash
# 1. 刪除 data_out 中的所有檔案
rm data_out/*

# 2. 重新執行清洗 → 抽取 → 審核 → 導入
python cli.py clean --input ./data_in --output ./data_out
python cli.py extract --input ./data_out --review-mode
python cli.py import --input ./data_out --chroma-db-path ../../backend/chroma_db
```

### 情況 3：只想更新部分逐字稿
```bash
# 1. 在 data_in 中只放入新增或修改的逐字稿
# 2. 執行清洗和抽取
python cli.py clean --input ./data_in --output ./data_out
python cli.py extract --input ./data_out

# 3. 在審核 UI 中檢視新增項目
# 4. 確認後導入（會覆蓋舊項目）
python cli.py import --input ./data_out --chroma-db-path ../../backend/chroma_db
```

---

## 工具設定

### 環境變數（可選）
```bash
# .env.tools
REVIEW_UI_PORT=8000  # 審核 UI 的埠號
CHROMA_DB_PATH=../../backend/chroma_db  # ChromaDB 路徑
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

### 依賴安裝
```bash
# 假設您已經有主應用的 Python 環境
cd tools/data_preparation
pip install -r requirements.txt
```

---

## 故障排除

| 問題 | 原因 | 解決方案 |
|------|------|--------|
| `No such file or directory: data_in` | 資料夾不存在 | 執行 `mkdir -p data_in data_out` |
| `cleaneded_*.json 為空` | 輸入檔案不符格式 | 確保輸入為 .txt 或 .md 格式 |
| 審核 UI 無法打開 | 埠 8000 被佔用 | 改用 `--review-ui-port 8001` |
| ChromaDB 導入失敗 | 路徑不正確 | 檢查 `--chroma-db-path` 是否指向正確的 ChromaDB 資料夾 |
| 知識無法在應用中搜尋 | 導入後沒有重啟應用 | 重啟 TurnFix 應用或點擊「重新加載知識庫」 |

---

## 支援和反饋

如有問題，請檢查：
1. 本指南的「常見情況」章節
2. 工具生成的報告（`validation_report.txt`、`import_report.txt`）
3. 應用的系統日誌（`backend/logs/`）
4. 提交 Issue 到 GitHub（附上報告和錯誤訊息）

---

**最後更新**：2025-10-28
**版本**：v1.0 (Planning)
