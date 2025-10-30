# 釐清問題

`SymptomPracticeMapping` 關聯表是否需要額外屬性（例如排序權重）或邏輯來處理練習卡數量限制（3-5 張）？

# 定位

ERM: SymptomPracticeMapping

# 多選題

| 選項 | 描述 |
|---|---|
| A | 是，需要額外屬性，例如 `weight` 或 `order` 來處理排序 |
| B | 是，需要額外邏輯來確保每個症狀對應 3-5 張練習卡 |
| C | 兩者都需要 |
| D | 兩者都不需要，目前設計已足夠 |
| Short | 提供其他簡短答案（<=5 字）|

# 影響範圍

影響 `SymptomPracticeMapping` 表格的設計，以及「建議生成」功能的複雜度與彈性。

# 優先級

Medium

---
# 解決記錄

- **回答**：C - 兩者都需要（額外屬性與額外邏輯）
- **更新的規格檔**：spec/erm.dbml
- **變更內容**：在 SymptomPracticeMapping 實體中新增 order 屬性，並更新註解說明需要額外邏輯來確保數量限制。