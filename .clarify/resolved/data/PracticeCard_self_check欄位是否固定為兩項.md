# 釐清問題

PracticeCard.self_check 欄位是否固定為兩項？

# 定位

ERM: PracticeCard.self_check[2]

# 多選題

| 選項 | 描述 |
|---|---|
| A | 是，固定為 2 項 |
| B | 否，是可變動數量的列表，最多 2 項 |
| C | 否，是可變動數量的列表，無上限 |
| Short | 提供其他簡短答案（<=5 字）|

# 影響範圍

影響練習卡（PracticeCard）的資料結構定義與前端顯示邏輯。如果為可變數量，需考慮 UI 如何適應不同數量的自我檢查點。

# 優先級

Medium

---
# 解決記錄

- **回答**：可變動，上限 3 個
- **更新的規格檔**：spec/erm.dbml
- **變更內容**：在 PracticeCard 實體中更新 self_check 註解