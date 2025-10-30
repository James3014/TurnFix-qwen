# TurnFix 資料處理工具集

本目錄包含用於處理和準備滑雪教學資料的工具集，實現了從原始資料到知識庫的完整處理流程。

## 工具列表

### 1. 逐字稿清洗工具 (TOOL-101)
用於清洗逐字稿和教練回答，準備用於後續處理。

```bash
# 清洗單個文件
python tools/data_preparation/cli.py clean -i input.txt -o output.json

# 批量清洗目錄中的文件
python tools/data_preparation/cli.py clean -i /path/to/input_dir -o /path/to/output_dir

# 指定最大段落長度
python tools/data_preparation/cli.py clean -i input.txt -o output.json -m 800
```

### 2. 知識抽取工具 (TOOL-102)
從清洗後的資料中自動抽取症狀和練習建議。

```bash
# 從單個文件抽取知識
python tools/data_preparation/cli.py extract -i input.json -o output.json

# 批量抽取目錄中的文件
python tools/data_preparation/cli.py extract -i /path/to/input_dir -o /path/to/output_dir
```

### 3. 資料驗證工具 (TOOL-103)
檢查資料品質並生成驗證報告。

```bash
# 生成驗證報告
python tools/data_preparation/cli.py validate -i /path/to/input_dir -o validation_report.json
```

### 4. 人工審核界面 (TOOL-104)
Web 界面用於人工審核自動抽取的知識片段。

前端組件位於 `frontend/components/ReviewInterface.js`，可整合到管理後台。

### 5. 知識導入工具 (TOOL-105)
將審核後的知識片段導入向量數據庫。

```bash
# 導入審核後的知識片段
python tools/data_preparation/cli.py import -i approved_knowledge.json -r import_report.json
```

## Web API 接口 (TOOL-107)

除了命令行工具，還提供了 Web API 接口用於管理知識庫：

- `POST /api/v1/knowledge/upload` - 上傳清洗後的JSON檔案
- `GET /api/v1/knowledge/list-pending-review` - 獲取待審核知識片段列表
- `POST /api/v1/knowledge/approve/{id}` - 批准知識片段
- `POST /api/v1/knowledge/reject/{id}` - 拒絕知識片段
- `GET /api/v1/knowledge/export` - 導出已批准的知識片段

## 使用流程

1. **資料清洗**: 使用 `cli.py clean` 命令清洗原始資料
2. **知識抽取**: 使用 `cli.py extract` 命令從清洗後的資料抽取知識
3. **品質驗證**: 使用 `cli.py validate` 命令檢查資料品質
4. **人工審核**: 
   - 通過 Web API 或人工審核界面審核抽取的知識
   - 批准或拒絕知識片段
5. **知識導入**: 使用 `cli.py import` 命令將批准的知識導入向量數據庫

## 資料格式

### 輸入格式 (清洗後)
```json
{
  "metadata": {
    "source_file": "coach_response_001.txt",
    "language": "zh",
    "processing_timestamp": "2025-10-29T10:00:00Z"
  },
  "segments": [
    "滑雪時重心太後會導致後坐，...",
    "換刃困難通常是因為壓力轉移不夠，..."
  ]
}
```

### 知識片段格式
```json
{
  "symptom": "重心太後",
  "practice_tips": ["保持上身直立", "重心向前移"],
  "pitfalls": ["避免後坐", "不要過度彎曲膝蓋"],
  "dosage": "藍線6次/趟×3趟",
  "source_snippet": "當重心太後時，會導致後坐...",
  "confidence": 0.85,
  "review_status": "pending"
}
```