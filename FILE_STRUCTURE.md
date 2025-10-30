# TurnFix 專案文件結構

**最後更新**：2025-10-28
**狀態**：整理完成 ✅

---

## 📁 根目錄文件清單 (14 個核心文件)

### 🔴 必讀核心文件 (5 個)

這些是專案的重要規格和計劃文件，所有團隊成員都應該了解。

| 文件 | 大小 | 用途 | 讀者 |
|------|------|------|------|
| **tasks.md** | 35K | 💼 完整任務清單，包含所有 UI/API/測試任務 | 全體 |
| **sdd-TurnFix.md** | 11K | 📋 系統設計文檔 (System Design Document) | PM, 開發者 |
| **plan.md** | 10K | 📅 實施計劃與時間表 | PM, 項目經理 |
| **README.md** | 3.9K | 📖 項目概覽與快速開始 | 新加入成員 |
| **architecture.md** | 19K | 🏗️ 系統架構與技術棧 | 開發者 |

### 🟢 回饋系統核心設計 (6 個)

這些文件包含完整的回饋系統設計（用戶層 + 管理層）。

| 文件 | 大小 | 用途 | 優先級 |
|------|------|------|--------|
| **ADMIN_FEEDBACK_ANALYTICS_DESIGN.md** | 26K | ⭐ 管理後台詳細設計 (UI-308.6-10, API-207) | 🔴 必讀 |
| **ADMIN_ANALYTICS_QUICK_GUIDE.md** | 10K | ⭐ 管理員操作手冊 | 🔴 管理員必讀 |
| **STAR_RATING_FEEDBACK_DESIGN.md** | 13K | ⭐ 星數評分系統完整設計 (用戶層) | 🟡 參考 |
| **COMPLETE_FEEDBACK_SYSTEM_SUMMARY.md** | 15K | ⭐ 回饋系統總體總結 | 🟡 參考 |
| **FEEDBACK_ANALYTICS_INTEGRATION_SUMMARY.md** | 12K | ⭐ 集成總結與實施計劃 | 🟡 參考 |
| **FEEDBACK_DOCS_NAVIGATION.md** | 9.0K | 🧭 文檔導航 - 快速定位 | 🟢 快速參考 |

### 🟡 參考與工具文件 (3 個)

這些文件提供補充信息和開發支持。

| 文件 | 大小 | 用途 |
|------|------|------|
| **STAR_RATING_QUICK_REFERENCE.md** | 7.8K | ⚡ API 速查表、SQL 示例、測試用例 |
| **dev-setup.md** | 8.4K | 🛠️ 開發環境配置指南 |
| **LINUS_GUIDE.md** | 5.7K | 💡 設計原則 (簡潔、務實、避免過度工程) |

---

## 📦 _archive 目錄文件說明

這些文件已移至歸檔目錄。它們記錄了設計演進過程，如有需要可查閱。

```
_archive/deprecated/
├── CLARIFICATION_SUMMARY.md (17K)       [舊版] 澄清總結
├── FEEDBACK_DESIGN_UPDATE.md (6.3K)     [過程] 設計更新記錄
├── FEEDBACK_SYSTEM_EVOLUTION.md (6.7K)  [過程] 設計演進說明
├── IMPLEMENTATION_SUMMARY.md (10K)      [舊版] 實施總結
├── DATA_PREP_TOOL_GUIDE.md (8.7K)       [未來] 數據準備工具指南
├── TWO_TIER_FEEDBACK_DESIGN.md (14K)    [舊版] 三選項系統設計
├── UI_Design_Brief.md (3.8K)            [舊版] UI 概覽
└── CONTRIBUTING.md (1.2K)               [初期] 貢獻指南
```

**為什麼被歸檔**：
- 內容已並入新的核心設計文檔
- 記錄了設計演進過程，但當前不需要持續參考
- 星數系統已升級，舊的三選項設計不再使用

**何時查閱**：
- 想了解設計決策過程 → FEEDBACK_DESIGN_UPDATE.md
- 想了解設計演進歷史 → FEEDBACK_SYSTEM_EVOLUTION.md
- 想看舊版設計 → TWO_TIER_FEEDBACK_DESIGN.md

---

## 🎯 按角色推薦的文件閱讀順序

### 👨‍💻 開發工程師

**第一天** (必讀，2-3 小時)：
```
1. README.md (5 min) - 項目概覽
2. architecture.md (20 min) - 系統架構
3. tasks.md (30 min) - 查看你負責的任務
4. ADMIN_FEEDBACK_ANALYTICS_DESIGN.md (60 min) - 詳細規格
```

**第二天** (參考)：
```
5. STAR_RATING_QUICK_REFERENCE.md - API 速查
6. dev-setup.md - 開發環境配置
```

### 👥 管理員 / 教練

**上線前培訓** (45 分鐘)：
```
1. README.md (5 min)
2. ADMIN_ANALYTICS_QUICK_GUIDE.md (40 min) - 完整閱讀
```

**日常操作**：
```
- ADMIN_ANALYTICS_QUICK_GUIDE.md 的「快速決策場景」
```

### 📊 產品經理

**評估與計劃** (1-2 小時)：
```
1. sdd-TurnFix.md (20 min) - 系統設計
2. COMPLETE_FEEDBACK_SYSTEM_SUMMARY.md (30 min) - 系統總結
3. FEEDBACK_ANALYTICS_INTEGRATION_SUMMARY.md (30 min) - 集成計劃
4. ADMIN_FEEDBACK_ANALYTICS_DESIGN.md (20 min) - 案例分析
```

### 🏢 決策者 / 執行者

**決策評估** (20-30 分鐘)：
```
1. README.md (5 min)
2. COMPLETE_FEEDBACK_SYSTEM_SUMMARY.md (15 min) - 關鍵信息
3. FEEDBACK_ANALYTICS_INTEGRATION_SUMMARY.md (10 min) - 實施計劃
```

---

## 📊 文件關係圖

```
核心規格
├─ sdd-TurnFix.md (系統設計)
├─ tasks.md (任務分解)  ← 所有任務都來自這裡
└─ plan.md (實施計劃)

回饋系統設計
├─ STAR_RATING_FEEDBACK_DESIGN.md (用戶層)
│   ├─ 星數系統 (⭐1-5)
│   ├─ API-204 & API-206
│   └─ UI-307 & UI-309
│
└─ ADMIN_FEEDBACK_ANALYTICS_DESIGN.md (管理層) ⭐ 核心
    ├─ 儀表板 (UI-308.6)
    ├─ 詳細分析 (UI-308.7-9)
    ├─ API-207 (6 個端點)
    └─ 數據驅動決策

集成與總結
├─ COMPLETE_FEEDBACK_SYSTEM_SUMMARY.md (全景視圖)
├─ FEEDBACK_ANALYTICS_INTEGRATION_SUMMARY.md (實施計劃)
└─ FEEDBACK_DOCS_NAVIGATION.md (快速導航) ← 快速定位

參考資源
├─ STAR_RATING_QUICK_REFERENCE.md (快速查閱)
├─ architecture.md (系統架構)
├─ LINUS_GUIDE.md (設計原則)
└─ dev-setup.md (開發環境)
```

---

## ✅ 清理完成項目

### 已完成的整理工作

- ✅ 識別並移動 8 個過時/歸檔文件
- ✅ 保留 14 個核心和參考文件在根目錄
- ✅ 建立 _archive/deprecated 目錄存放歷史文檔
- ✅ 建立本文件 (FILE_STRUCTURE.md)

### 目錄結構現狀

```
TurnFix/
├── 📋 核心規格文件 (5)
│   ├── tasks.md ⭐ 最重要
│   ├── sdd-TurnFix.md
│   ├── plan.md
│   ├── README.md
│   └── architecture.md
│
├── 🎯 回饋系統設計 (6)
│   ├── ADMIN_FEEDBACK_ANALYTICS_DESIGN.md ⭐ 管理層
│   ├── ADMIN_ANALYTICS_QUICK_GUIDE.md
│   ├── STAR_RATING_FEEDBACK_DESIGN.md
│   ├── COMPLETE_FEEDBACK_SYSTEM_SUMMARY.md
│   ├── FEEDBACK_ANALYTICS_INTEGRATION_SUMMARY.md
│   └── FEEDBACK_DOCS_NAVIGATION.md
│
├── 🛠️ 工具與參考 (3)
│   ├── STAR_RATING_QUICK_REFERENCE.md
│   ├── dev-setup.md
│   └── LINUS_GUIDE.md
│
├── 📦 _archive/ (歷史文件)
│   └── deprecated/
│       ├── CLARIFICATION_SUMMARY.md
│       ├── FEEDBACK_DESIGN_UPDATE.md
│       ├── FEEDBACK_SYSTEM_EVOLUTION.md
│       ├── IMPLEMENTATION_SUMMARY.md
│       ├── DATA_PREP_TOOL_GUIDE.md
│       ├── TWO_TIER_FEEDBACK_DESIGN.md
│       ├── UI_Design_Brief.md
│       └── CONTRIBUTING.md
│
├── 🗂️ 其他目錄
│   ├── spec/ (erm.dbml, features/)
│   ├── UI/ (UI 設計文件)
│   ├── /tools/ (工具)
│   └── ...
```

---

## 🔍 快速找文件

### 我需要 API 規格？
→ **ADMIN_FEEDBACK_ANALYTICS_DESIGN.md** (Section: 🔌 API 設計詳解)
→ **STAR_RATING_QUICK_REFERENCE.md** (API 速查表)

### 我需要 UI 設計？
→ **ADMIN_FEEDBACK_ANALYTICS_DESIGN.md** (Section: 🎨 UI 設計)

### 我需要任務清單？
→ **tasks.md** (所有 UI/API/測試任務)

### 我需要實施計劃？
→ **plan.md** 或 **FEEDBACK_ANALYTICS_INTEGRATION_SUMMARY.md**

### 我需要開發環境設置？
→ **dev-setup.md**

### 我想快速了解整個系統？
→ **FEEDBACK_DOCS_NAVIGATION.md** (按角色推薦)

### 我想查看設計演進過程？
→ **_archive/deprecated/FEEDBACK_DESIGN_UPDATE.md**

---

## 💡 建議

1. **新團隊成員**：
   - 從 README.md 開始
   - 然後根據角色閱讀推薦文件

2. **開發開始前**：
   - 確保已讀 tasks.md 和 sdd-TurnFix.md
   - 查看 ADMIN_FEEDBACK_ANALYTICS_DESIGN.md 的相關 section

3. **尋找特定信息**：
   - 使用 FEEDBACK_DOCS_NAVIGATION.md 定位
   - 使用 STAR_RATING_QUICK_REFERENCE.md 快速查詢 API

4. **管理員上線**：
   - 參閱 ADMIN_ANALYTICS_QUICK_GUIDE.md
   - 參加 30-45 分鐘的培訓會議

---

## 📝 備註

- 所有核心文件都在根目錄，易於定位
- _archive 目錄保存歷史，不會干擾日常工作
- 文件間相互引用清晰，便於導航
- 根據不同角色有推薦閱讀順序

---

**版本**：v1.0
**更新日期**：2025-10-28
**狀態**：整理完成，結構清晰 ✅
