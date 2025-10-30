# 釐清問題

Session.slots 欄位的資料結構為何？

# 定位

ERM: Session.slots

# 多選題

| 選項 | 描述 |
|---|---|
| A | 一個 JSON 物件，如 {"level": "初級", "terrain": "綠線"} |
| B | 一個簡單的字串，如 "初級, 綠線" |
| C | 分開儲存為多個欄位，如 `level_slot`, `terrain_slot` |
| Short | 提供其他簡短答案（<=5 字）|

# 影響範圍

影響 Session 資料表的設計以及後續對使用者輸入條件的分析能力。結構化資料（A 或 C）優於非結構化字串。

# 優先級

Medium

---
# 解決記錄

- **回答**：C - 分開儲存為多個獨立欄位，例如 `level_slot`, `terrain_slot`, `style_slot`
- **更新的規格檔**：spec/erm.dbml
- **變更內容**：從 Session 實體中移除 slots 欄位，並新增 level_slot, terrain_slot, style_slot 欄位。