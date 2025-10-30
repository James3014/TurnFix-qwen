# 釐清問題

PracticeCard.pitfalls 欄位是單一字串還是字串列表？

# 定位

ERM: PracticeCard.pitfalls

# 多選題

| 選項 | 描述 |
|---|---|
| A | 單一字串（一個常見錯誤） |
| B | 字串列表（多個常見錯誤） |
| Short | 提供其他簡短答案（<=5 字）|

# 影響範圍

影響 PracticeCard 的資料結構與前端渲染。若為列表，UI 需支援多點顯示。

# 優先級

Low

---
# 解決記錄

- **回答**：A - 單一文字，代表一個常見錯誤
- **更新的規格檔**：spec/erm.dbml
- **變更內容**：在 PracticeCard 實體中更新 pitfalls 註解