# 釐清問題

PracticeCard.dosage 欄位的具體格式為何？

# 定位

ERM: PracticeCard.dosage

# 多選題

| 選項 | 描述 |
|---|---|
| A | 自由文字，如「藍線 6 次/趟 ×3 趟」 |
| B | 結構化物件，如 {terrain: '藍線', reps: 6, sets: 3} |
| C | 僅包含次數與趟數的字串，如 "6x3" |
| Short | 提供其他簡短答案（<=5 字）|

# 影響範圍

影響 PracticeCard 的資料庫欄位型別（String vs. JSON）與前端解析渲染方式。結構化資料更利於未來的功能擴充（如數據分析）。

# 優先級

Medium

---
# 解決記錄

- **回答**：A - 自由文字，例如「藍線 6 次/趟 ×3 趟」
- **更新的規格檔**：spec/erm.dbml
- **變更內容**：在 PracticeCard 實體中更新 dosage 註解