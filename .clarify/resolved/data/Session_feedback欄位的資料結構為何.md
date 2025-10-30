# 釐清問題

Session.feedback 欄位的資料結構為何？

# 定位

ERM: Session.feedback

# 多選題

| 選項 | 描述 |
|---|---|
| A | 一個 JSON 物件，如 {"rating": "👍", "text": "很有幫助"} |
| B | 一個簡單的字串，用於儲存自由文字回饋 |
| C | 分開儲存為 `feedback_rating` 和 `feedback_text` 兩個欄位 |
| Short | 提供其他簡短答案（<=5 字）|

# 影響範圍

影響 Session 資料表的設計以及對使用者回饋的分析和查詢能力。結構化資料（A 或 C）更易於統計分析。

# 優先級

Medium

---
# 解決記錄

- **回答**：C - 分開儲存為 `feedback_rating` 和 `feedback_text` 兩個獨立欄位
- **更新的規格檔**：spec/erm.dbml
- **變更內容**：從 Session 實體中移除 feedback 欄位，並新增 feedback_rating 和 feedback_text 欄位。