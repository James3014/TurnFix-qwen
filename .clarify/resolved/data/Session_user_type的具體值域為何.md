# 釐清問題

Session.user_type 的具體值域為何？

# 定位

ERM: Session.user_type

# 多選題

| 選項 | 描述 |
|---|---|
| A | '學員', '教練' |
| B | 'student', 'coach' |
| C | 數字 1, 2 代表 |
| Short | 提供其他簡短答案（<=5 字）|

# 影響範圍

影響 Session 資料表的欄位定義與未來可能的使用者行為分析。

# 優先級

Low

---
# 解決記錄

- **回答**：A - 「學員」或「教練」
- **更新的規格檔**：spec/erm.dbml
- **變更內容**：在 Session 實體中更新 user_type 註解