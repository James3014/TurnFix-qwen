# TurnFix 雙層回饋 + 最愛清單 設計文檔

## 📋 核心概念

TurnFix 採用**雙層回饋系統**來收集不同維度的用戶反饋，以及**最愛清單**功能便於用戶快速存取常用練習卡。

```
使用者流程：
   ↓
問題描述 → 系統推薦練習卡們
   ↓
[回饋層一] 這些練習卡有幫助嗎？(Session 層級)
   ↓
查看/執行練習卡
   ↓
[回饋層二] 這張練習卡有幫助嗎？(PracticeCard 層級)
   ↓
[可選] ❤️ 加入最愛清單
   ↓
未來快速存取最愛清單中的常用練習卡
```

---

## 🔄 回饋層一：Session 層級 - 整體推薦效果評價

### 目的
評估系統推薦的**整套練習卡**是否有助於解決用戶的**原始問題**。

### 時機

**即時回饋**：
- 用戶收到推薦後，可直接評價
- 適合那些對推薦品質有明確看法的用戶
- UI 位置：推薦結果頁面底部

**延遲回饋**：
- 用戶可在練習一段時間後（1-2 週）回溯評價
- 適合需要實踐一段時間才能判斷效果的用戶
- UI 位置：歷史記錄頁面，每個會話可點擊「評價」

### 三個評分選項

| 選項 | Emoji | 含義 | 用戶場景 |
|------|-------|------|---------|
| **不適用** | ❌ | 推薦的練習卡與我的問題無關或不適合 | 症狀被誤辨識、等級/地形不對 |
| **部分適用** | △ | 推薦有幫助，但改善不夠明顯或需要補充 | 部分練習有效、但整體効果一般 |
| **適用** | ✓ | 推薦的練習卡很有幫助，明顯改善了我的問題 | 完全符合需求、效果顯著 |

### 資料模型

```sql
CREATE TABLE SessionFeedback (
  id INT PRIMARY KEY,
  session_id INT NOT NULL,  -- 對應的會話
  rating VARCHAR(20),        -- 值域：not_applicable / partially_applicable / applicable
  feedback_text TEXT,        -- 自由文字回饋（可選）
  feedback_type VARCHAR(20), -- 值域：immediate / delayed
  created_at TIMESTAMP,
  FOREIGN KEY (session_id) REFERENCES Session(id),
  UNIQUE (session_id)        -- 一個會話最多一條 SessionFeedback
);
```

### API 設計

**POST /api/v1/sessions/{session_id}/feedback**
```json
// 請求
{
  "rating": "applicable",                      // ✓ 適用
  "feedback_text": "這些練習卡很有幫助！",
  "feedback_type": "immediate"                 // 或 "delayed"
}

// 回應
{
  "success": true,
  "message": "感謝您的回饋！",
  "feedback_id": 123,
  "recorded_at": "2025-10-28T14:30:00Z"
}
```

**GET /api/v1/sessions/{session_id}/feedback**
```json
// 回應
{
  "session_id": 123,
  "rating": "applicable",
  "feedback_text": "這些練習卡很有幫助！",
  "feedback_type": "immediate",
  "created_at": "2025-10-28T14:30:00Z"
}
```

---

## 📌 回饋層二：PracticeCard 層級 - 單個練習卡評價

### 目的
評估**單個練習卡本身**的品質和實用性，獨立於是否改善了整體問題。

### 時機

隨時可評價：
- 用戶在「我的練習」中查看已執行過的練習卡時
- 用戶在練習卡詳細頁面時（無論是否最近推薦的）
- 支援多次修改已給過的評分

### 三個評分選項

| 選項 | Emoji | 含義 | 用戶場景 |
|------|-------|------|---------|
| **不適用** | ❌ | 這張練習卡對我無幫助或不適合 | 步驟不清楚、難度不對、已掌握 |
| **部分適用** | △ | 這張練習卡有幫助，但需要調整或補充 | 步驟需簡化、建議改進、有小問題 |
| **適用** | ✓ | 這張練習卡很有幫助，完全符合我的需求 | 步驟清晰、正好難度、非常有效 |

### 加入最愛清單

評分完成後，用戶可選擇「❤️ 加入最愛清單」：
- 標記此練習卡為「常用」或「有效」
- 便於未來快速存取
- 可在評分後任何時間點擊按鈕加入/移除

### 資料模型

```sql
CREATE TABLE PracticeCardFeedback (
  id INT PRIMARY KEY,
  session_id INT NOT NULL,    -- 來自哪個會話（可能為 NULL，如果是獨立評價）
  practice_id INT NOT NULL,   -- 評價的練習卡
  rating VARCHAR(20),          -- 值域：not_applicable / partially_applicable / applicable
  feedback_text TEXT,          -- 自由文字回饋（可選）
  is_favorite BOOLEAN,         -- 是否加入最愛清單
  created_at TIMESTAMP,
  updated_at TIMESTAMP,        -- 支援修改評分
  FOREIGN KEY (session_id) REFERENCES Session(id),
  FOREIGN KEY (practice_id) REFERENCES PracticeCard(id),
  UNIQUE (session_id, practice_id)  -- 一個會話只能對一個練習卡評分一次
);
```

### API 設計

**POST /api/v1/practice-cards/{practice_id}/feedback**
```json
// 請求
{
  "session_id": 123,                           // 可選，來自哪個會話
  "rating": "applicable",                      // ✓ 適用
  "feedback_text": "步驟很清楚，非常有幫助！",
  "is_favorite": false                         // 是否同時加入最愛
}

// 回應
{
  "success": true,
  "message": "感謝您的回饋！",
  "feedback_id": 456,
  "recorded_at": "2025-10-28T14:35:00Z"
}
```

**PUT /api/v1/practice-card-feedback/{feedback_id}**
```json
// 請求（修改評分）
{
  "rating": "partially_applicable",
  "feedback_text": "重新練習後，發現步驟需要調整",
  "is_favorite": true                          // 同步更新最愛狀態
}

// 回應
{
  "success": true,
  "message": "回饋已更新",
  "updated_at": "2025-10-28T15:00:00Z"
}
```

**GET /api/v1/practice-cards/{practice_id}/feedback**
```json
// 回應（獲取該練習卡的所有評分統計）
{
  "practice_id": 456,
  "rating_distribution": {
    "not_applicable": 2,
    "partially_applicable": 5,
    "applicable": 18
  },
  "average_helpfulness": 0.75,                 // 計算方式：applicable count / total count
  "favorite_count": 8,                         // 加入最愛的人數
  "user_feedback": {                           // 當前用戶的反饋
    "rating": "applicable",
    "feedback_text": "...",
    "is_favorite": true,
    "created_at": "2025-10-28T14:35:00Z"
  }
}
```

---

## ⭐ 最愛清單功能

### 目的

建立一個**個人化的「常用練習卡庫」**，便於：
1. **快速存取**：找到身邊最常用、最有效的練習卡
2. **疲憊時救援**：當身體疲憊/時間緊張時，直接存取最愛清單而不用經過整個推薦流程
3. **系統優化**：幫助系統了解哪些練習卡最被用戶認可

### 加入方式

**方式一：評分時直接加入**
```
練習卡評分 → 選擇評分 → 「加入最愛清單」按鈕
```

**方式二：練習卡詳細頁面的星按鈕**
```
練習卡詳細頁面 → 上方「★ 加入最愛」按鈕（點擊切換）
```

**方式三：歷史記錄中標記**
```
我的練習 → 歷史記錄 → 點擊練習卡 → 「★ 加入最愛」
```

### 資料模型

最愛狀態儲存在 `PracticeCardFeedback.is_favorite` 字段：
- 用戶對一張練習卡只能有一條 `PracticeCardFeedback` 記錄
- `is_favorite` 布林值表示該卡是否在最愛清單中

### API 設計

**POST/PUT /api/v1/practice-cards/{practice_id}/favorite**
```json
// 請求
{
  "is_favorite": true  // 加入最愛（true） 或 移除最愛（false）
}

// 回應
{
  "success": true,
  "message": "已加入最愛清單",
  "practice_id": 456,
  "is_favorite": true,
  "updated_at": "2025-10-28T15:05:00Z"
}
```

**GET /api/v1/my-practice/favorites**
```json
// 回應（列出所有最愛練習卡）
{
  "total": 8,
  "favorites": [
    {
      "practice_id": 456,
      "name": "J 型轉彎",
      "category": "轉彎技巧",
      "goal": "完成外腳承重再過中立",
      "my_feedback": {
        "rating": "applicable",
        "feedback_text": "非常有幫助！",
        "created_at": "2025-10-28T14:35:00Z"
      },
      "added_to_favorite_at": "2025-10-28T14:35:00Z"
    },
    ...
  ]
}
```

**DELETE /api/v1/practice-cards/{practice_id}/favorite**
```json
// 請求（移除最愛）
{
  "is_favorite": false
}

// 回應
{
  "success": true,
  "message": "已從最愛清單移除",
  "practice_id": 456,
  "is_favorite": false
}
```

---

## 🎨 UI 流程圖

### 推薦結果頁面（UI-303）

```
┌─────────────────────────────────┐
│   3-5 張推薦練習卡展示            │
│   （按關聯性排序）                │
│                                 │
│   [卡片 1] [卡片 2] [卡片 3]   │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│  【回饋層一】                     │
│  這些練習卡有幫助嗎？              │
│                                 │
│  [❌不適用] [△部分] [✓適用]    │ ← UI-307.1.1
│                                 │
│  其他建議？                       │
│  [文字輸入框.....................] │
│                                 │
│            [提交] [稍後評價]     │
└─────────────────────────────────┘
```

### 練習卡詳細頁面（UI-304）

```
┌─────────────────────────────────┐
│ ← 回上頁      ★ 加入最愛 ↑      │ ← UI-304.4
├─────────────────────────────────┤
│ 練習卡名稱                        │
│ 目標、要點、常見錯誤等內容        │
│                                 │
│ 進度條：66%                      │
│                                 │
│ [要點清單] [自我檢查點]          │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│  【回饋層二】                     │
│  這個練習卡有幫助嗎？              │
│                                 │
│  [❌不適用] [△部分] [✓適用]    │ ← UI-307.2.1
│                                 │
│  你有其他建議嗎？                 │
│  [文字輸入框.....................] │
│                                 │
│  [❤️ 加入最愛清單] (可選)       │ ← UI-307.2.1
│                                 │
│            [提交回饋]            │
└─────────────────────────────────┘
```

### 最愛清單頁面（UI-309）

```
┌─────────────────────────────────┐
│ 我的練習 > 最愛          (8)    │
├─────────────────────────────────┤
│                                 │
│ [✓ 適用] J 型轉彎              │
│ 評分時間：2025-10-25           │
│ 我的評價：非常有幫助！           │
│ [立即練習] [❤️ 移除] [查看評價]  │
│                                 │
├─────────────────────────────────┤
│ [△ 部分適用] 基礎轉彎           │
│ 評分時間：2025-10-22           │
│ 我的評價：有幫助但需要改進       │
│ [立即練習] [❤️ 移除] [查看評價]  │
│                                 │
├─────────────────────────────────┤
│ ... 更多最愛練習卡 ...           │
│                                 │
└─────────────────────────────────┘
```

---

## 📊 數據收集和分析

### 系統側的數據應用

**回饋層一的數據**：
- 評估推薦算法的準確性
- 識別被誤辨識的症狀
- 優化症狀→練習卡的映射關係

**回饋層二的數據**：
- 識別「高品質」的練習卡（適用比例高）
- 識別「需要改進」的練習卡（部分適用較多）
- 識別「過時」的練習卡（不適用率高）

**最愛清單的數據**：
- 哪些練習卡最被用戶推崇
- 用戶的個性化偏好
- 建議在系統推薦時「提升評分高的練習卡的排名」

### 分析儀表板（管理後台計劃功能）

```
【練習卡品質分析】
- 適用率：18 / 25 = 72%  ✓ 高品質
- 加入最愛數：8 人        ✓ 受歡迎
- 平均評分：△ 0.75 分    ⚠ 可考慮改進

【症狀推薦準確度】
- 症狀「後坐」：
  - 推薦次數：45
  - 整體回饋適用率：68%  ⚠ 需改進
  - 常見問題：「地形選擇不對」

【用戶最愛排名】
1. J 型轉彎（10 人標記）
2. 基礎轉彎（8 人標記）
3. 重心穩定（7 人標記）
```

---

## ✅ 實作檢查清單

### 資料庫層
- [ ] 建立 `SessionFeedback` 表
- [ ] 建立 `PracticeCardFeedback` 表
- [ ] 更新 `Session` 表移除舊的 `feedback_rating` 欄位（或保留用於遷移）

### API 層
- [ ] **API-204.1**：POST SessionFeedback
- [ ] **API-204.2**：GET SessionFeedback
- [ ] **API-204.3**：POST PracticeCardFeedback
- [ ] **API-204.4**：PUT PracticeCardFeedback（修改評分）
- [ ] **API-204.5**：GET PracticeCardFeedback（統計數據）
- [ ] **API-206.1**：GET 我的最愛清單
- [ ] **API-206.2**：POST/PUT 更新最愛狀態
- [ ] **API-206.3**：DELETE 移除最愛

### UI 層
- [ ] **UI-304.4**：練習卡詳細頁面的「★ 加入最愛」按鈕
- [ ] **UI-307.1.1**：推薦結果頁面的回饋層一
- [ ] **UI-307.1.2**：歷史記錄的延遲回饋機制
- [ ] **UI-307.2.1**：練習卡詳細頁面的回饋層二
- [ ] **UI-307.2.2**：支援修改評分
- [ ] **UI-309.1～4**：最愛清單頁面完整實作

### 測試
- [ ] 單個回饋的完整流程測試
- [ ] 最愛標記/取消標記測試
- [ ] 修改評分測試
- [ ] 延遲回饋場景測試
- [ ] 統計數據準確性測試

---

## 🔮 未來優化方向

1. **智能推薦**：根據用戶最愛清單自動推薦類似的練習卡
2. **趨勢分析**：分析用戶的偏好變化（從不適用 → 適用）
3. **社群排名**：展示「全球最愛」或「同等級最推薦」的練習卡
4. **個性化排序**：在推薦時優先顯示用戶最愛清單中的相關練習卡
5. **回饋提醒**：定時提醒用戶對近期推薦進行「延遲回饋」

---

**文檔版本**：v1.0
**更新日期**：2025-10-28
**狀態**：✅ 完整設計，可開始實作
