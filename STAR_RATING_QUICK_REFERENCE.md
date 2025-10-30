# 星數回饋系統 - 快速參考指南

**最後更新**：2025-10-28
**適用版本**：v2.0+

---

## ⚡ 核心概念 (30 秒速通)

```
什麼是星數回饋？
→ 用戶給予練習卡 1-5 顆星的實用評分

什麼是 is_favorite？
→ 獨立的「加入最愛」標記，可與星數分開操作

為什麼要獨立？
→ 用戶的需求場景不同：
  • 5★ ❤️ = 完全符合，經常用
  • 5★ = 完全符合，但暫不需要
  • 3★ ❤️ = 部分適用，想定期改進
```

---

## 📊 星數對照表

| 星數 | 含義 | UI 文案 | API 值 | 圖示 |
|------|------|--------|-------|------|
| **1** | 不適用 | 不適用 - 練習卡與我的症狀無關 | `1` | ⭐ |
| **2** | 較不適用 | 較不適用 - 部分內容有用 | `2` | ⭐⭐ |
| **3** | 部分適用 | 部分適用 - 有幫助但需要調整 | `3` | ⭐⭐⭐ |
| **4** | 適用 | 適用 - 相當有幫助 | `4` | ⭐⭐⭐⭐ |
| **5** | 非常適用 | 非常適用 - 完全符合我的需求 | `5` | ⭐⭐⭐⭐⭐ |

---

## 🔌 API 端點速查

### 1. 提交評分

```bash
POST /api/v1/practice-cards/{practice_id}/feedback

Body:
{
  "session_id": 123,           # 必須
  "rating": 4,                 # 必須 (1-5)
  "feedback_text": "optional"  # 可選
}

Response:
{
  "success": true,
  "feedback_id": 456,
  "rating": 4,
  "suggest_favorite": false    # 提示：rating >= 4 時為 true
}
```

### 2. 修改評分

```bash
PUT /api/v1/practice-cards/{practice_id}/feedback

Body:
{
  "rating": 5,                 # 修改為 5 顆星
  "feedback_text": "optional"
}

Response:
{
  "old_rating": 4,
  "new_rating": 5,
  "is_favorite": true          # 保持不變
}
```

### 3. 加入最愛

```bash
POST /api/v1/practice-cards/{practice_id}/favorite

Body:
{
  "action": "add"              # 或 "remove"
}

Response:
{
  "is_favorite": true,
  "current_rating": 4          # 返回當前星數（如有）
}
```

### 4. 獲取最愛清單

```bash
GET /api/v1/my-practice/favorites

Response:
[
  {
    "id": 123,
    "name": "練習卡名稱",
    "rating": 4,
    "feedback_text": "...",
    "is_favorite": true,
    "last_practiced": "2025-10-25",
    "marked_favorite_at": "2025-10-20"
  }
]
```

---

## 💾 數據庫相關

### 表結構

```sql
-- PracticeCardFeedback 表
CREATE TABLE PracticeCardFeedback (
  id INT PRIMARY KEY,
  session_id INT NOT NULL,
  practice_id INT NOT NULL,
  rating INT NOT NULL,          -- ⭐ 1-5
  feedback_text TEXT,           -- 可選
  is_favorite BOOLEAN DEFAULT false,
  created_at TIMESTAMP,
  UNIQUE(session_id, practice_id)
);
```

### 索引

```sql
-- 常用查詢優化
CREATE INDEX idx_practice_rating ON PracticeCardFeedback(practice_id, rating);
CREATE INDEX idx_favorite ON PracticeCardFeedback(session_id, is_favorite);
```

---

## 🎨 UI 實施檢查清單

### UI-307.2.1: 評分界面

```
□ 顯示 5 個星數按鈕
□ 點擊後高亮選中的星數
□ 顯示對應含義文案
□ ❤️ 按鈕位於下方（獨立操作）
□ 自由文字輸入框可選
□ [提交] 按鈕

Example:
┌─────────────────────┐
│ 這個練習卡對你有幫助嗎？
│
│ [⭐][⭐⭐][⭐⭐⭐][⭐⭐⭐⭐][⭐⭐⭐⭐⭐]
│
│ 你評分了 4 顆星 - 適用
│
│ ❤️ 加入最愛練習清單
│
│ 你有其他建議嗎？
│ [____________________]
│
│      [提交評分]
└─────────────────────┘
```

### UI-307.2.2: 修改評分

```
□ 用戶點擊不同星數可修改
□ 無需重新提交全部表單
□ 修改後立即保存
```

### UI-309.1: 最愛清單

```
□ 顯示卡片名稱
□ 顯示用戶給予的星數
□ 顯示評分備註
□ 顯示上次練習時間
□ [開始練習] 按鈕
□ [移除最愛] 按鈕（❤️）
□ [修改評分] 快速操作
```

---

## 🧪 測試用例

### TC-1: 基本評分流程

```
1. 用戶在練習卡詳情頁看到 5 個星數按鈕
2. 點擊 4 顆星 → 頁面顯示「你評分了 4 顆星 - 適用」
3. 點擊 [提交評分] → 評分保存成功
4. API 返回 suggest_favorite: false (因為 rating < 5)
```

### TC-2: 修改評分

```
1. 用戶之前評分為 4★
2. 用戶點擊 5 顆星重新評分
3. 頁面立即更新顯示 「5 顆星 - 非常適用」
4. API 返回 old_rating: 4, new_rating: 5
5. is_favorite 狀態保持不變
```

### TC-3: 加入最愛

```
1. 用戶評分為 4★，點擊 ❤️ 按鈕
2. ❤️ 按鈕高亮（顯示已加入最愛）
3. API 返回 is_favorite: true, current_rating: 4
4. 用戶之後修改評分為 3★
5. is_favorite 仍為 true（不受影響）
```

### TC-4: 獨立最愛操作

```
1. 用戶評分為 1★（不適用）
2. 用戶點擊 ❤️ 加入最愛
3. is_favorite 設為 true，星數保持 1★
4. 目的：追蹤「不適用」原因進行系統診斷
```

---

## 🔢 統計與分析

### 後台儀表板欄位

```
練習卡 ID: 123

平均星數: 4.2 / 5.0
評分總數: 156 次

分布：
┌─────────────────────────┐
│ 1★ (12)  ████░░░░░░  7.7%│
│ 2★ (8)   ███░░░░░░░░ 5.1%│
│ 3★ (28)  ████████░░░░ 17%│
│ 4★ (62)  ████████████████ 40%│
│ 5★ (46)  ██████████████ 29%│
└─────────────────────────┘

最愛次數: 89 / 156 (57%)
```

### 優化觸發條件

```
平均 ⭐⭐⭐⭐⭐ (5.0)    →   保留並優先推薦
平均 ⭐⭐⭐⭐ (4.0+)   →   正常推薦
平均 ⭐⭐⭐ (3.0)      →   標記「待改進」，收集建議
平均 ⭐⭐ (2.0)       →   檢查症狀匹配度
平均 ⭐ (1.0)        →   檢查是否誤推薦
```

---

## 🚨 常見問題與解決

### Q1: 如何區分「用戶未評分」和「評分為 1★」？

A: 檢查 `PracticeCardFeedback` 表：
```sql
-- 已評分
SELECT * FROM PracticeCardFeedback
WHERE practice_id = 123 AND session_id = 456
-- 有記錄且 rating = 1

-- 未評分
SELECT * FROM PracticeCardFeedback
WHERE practice_id = 123 AND session_id = 456
-- 無記錄
```

### Q2: 用戶同時修改星數和最愛狀態，順序如何？

A: 建議順序：
```
1. 先修改星數 (PUT /feedback)
2. 再修改最愛狀態 (POST /favorite)
```
或合併為單一 API 端點：
```
PATCH /api/v1/practice-cards/{id}/feedback-status
Body: { rating: 5, is_favorite: true }
```

### Q3: 如何統計「有評分的用戶佔比」？

A:
```sql
SELECT
  COUNT(DISTINCT session_id) as total_users,
  COUNT(DISTINCT CASE WHEN rating IS NOT NULL THEN session_id END) as rated_users,
  ROUND(COUNT(DISTINCT CASE WHEN rating IS NOT NULL THEN session_id END) * 100.0
        / COUNT(DISTINCT session_id), 2) as rating_rate_percent
FROM PracticeCardFeedback
WHERE practice_id = 123;
```

---

## 📋 部署檢查清單

### 上線前
- [ ] 資料庫遷移腳本測試通過
- [ ] 所有 API 端點經過壓力測試
- [ ] 前端 UI 在各種瀏覽器測試
- [ ] 用戶文案翻譯完成
- [ ] 備份所有舊資料

### 上線中
- [ ] 執行資料庫遷移
- [ ] 灰度發布 (10% 用戶先體驗)
- [ ] 實時監控 API 響應時間
- [ ] 監控錯誤率

### 上線後
- [ ] 收集初期用戶反饋
- [ ] 監控評分分布是否合理
- [ ] 監控最愛功能使用率
- [ ] 準備緊急回滾方案

---

## 🔗 相關文檔

| 深度 | 文檔 | 用途 |
|------|------|------|
| **入門** | 本文檔 | 快速查閱 |
| **詳細** | STAR_RATING_FEEDBACK_DESIGN.md | 完整設計規格 |
| **決策** | FEEDBACK_SYSTEM_EVOLUTION.md | 為什麼這樣設計 |
| **進度** | IMPLEMENTATION_SUMMARY.md | 實施計劃與進度 |
| **舊版** | TWO_TIER_FEEDBACK_DESIGN.md | 設計演進參考 |

---

**版本**：v1.0
**狀態**：發佈中
**最後更新**：2025-10-28
