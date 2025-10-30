# TurnFix 開發實施路線圖

**最後更新**：2025-10-28
**下一個檢查點**：2025-11-04（第一周完成檢查）

---

## 🗺️ 開發實施流程圖

```
開發流程順序
├── 第 0 周：環境準備
│   ├── 數據庫 schema 初始化 (DB-101 ~ DB-106)
│   ├── 後端環境配置 (DEV-601, DEV-603, DEV-604)
│   └── 前端環境配置 (DEV-602)
│
├── 第 1 周：核心反饋系統
│   ├── ✅ API-204.3-5：星數回饋端點 (4h)
│   ├── ✅ API-207.1-2：反饋統計 (4h)
│   ├── ✅ UI-307.2：星數評分界面 (4h)
│   ├── ✅ UXP-1801：進度追蹤 (4h) ← 平行進行
│   └── ✅ UXP-1802：推薦理由 (2h) ← 平行進行
│   = 共 18 小時，4 人工作 = 1 周完成
│
├── 第 2 周：管理後台第一期
│   ├── ✅ UI-308.6：儀表板 (6h)
│   ├── ✅ API-207.3-4：症狀和用戶分析 (6h)
│   ├── ✅ UI-308.7-8：詳細分析 (6h)
│   ├── ✅ UXP-P2：便利性提升 (8h) ← 平行進行
│   └── ✅ TEST-406.1-4：單元測試 (8h) ← 平行進行
│   = 共 34 小時，5 人工作 = 1 周完成
│
├── 第 3 周：完成管理後台 + UX 優化
│   ├── ✅ UI-308.9-10：用戶分析和導出 (6h)
│   ├── ✅ API-207.5-6：篩選和導出 (4h)
│   ├── ✅ TEST-406.5-7：集成測試 (6h)
│   ├── ✅ UXP-P3：習慣養成優化 (7h) ← 平行進行
│   └── ✅ 性能優化 (OPT-*) (6h) ← 平行進行
│   = 共 29 小時，5 人工作 = 1 周完成
│
└── 第 4 周：上線準備
    ├── ✅ UXP-P4：社群和趣味優化 (6h)
    ├── ✅ 完整回歸測試 (8h)
    ├── ✅ 安全檢查 (4h)
    ├── ✅ 管理員培訓資料準備 (4h)
    └── ✅ 上線前檢查清單
    = 共 22 小時，3 人工作 = 1 周完成
```

---

## 📋 詳細分解：第 1 周（核心反饋系統）

### 後端任務（開發者 A）- 8 小時

#### Day 1-2：API-204.3-5 星數回饋端點
```python
# tasks.py 中 API-204.3-5

POST /api/v1/feedback/practice-card
{
  "session_id": "...",
  "practice_id": 123,
  "rating": 4,  # 1-5
  "is_favorite": true,
  "comment": "清楚的步驟"
}

PUT /api/v1/feedback/practice-card/{feedback_id}
{
  "is_favorite": false  # 獨立更新最愛狀態
}

DELETE /api/v1/feedback/practice-card/{feedback_id}
```

**檢查清單**：
- [ ] 實現 PracticeCardFeedback 表的 CRUD
- [ ] 驗證星數範圍 (1-5)
- [ ] 支援 is_favorite 獨立更新
- [ ] 添加單元測試 (TEST-406.2)
- [ ] 測試不同邊界情況

#### Day 3：API-207.1-2 反饋統計端點
```python
# API-207.1：整體統計摘要

GET /api/v1/admin/feedback-analytics/summary
{
  "session_feedback_distribution": {
    "not_applicable": 12,
    "partially_applicable": 45,
    "applicable": 78
  },
  "rating_distribution": {
    1: 10, 2: 15, 3: 45, 4: 78, 5: 52
  },
  "average_rating": 3.8,
  "top_cards_by_rating": [...]
}

# API-207.2：單張卡片詳情

GET /api/v1/admin/feedback-analytics/practice-cards/123
{
  "card_info": {...},
  "rating_distribution": {...},
  "rating_trend": [...],  # 過去 30 天
  "feedback_comments": {...},
  "improvement_suggestions": [...]
}
```

**檢查清單**：
- [ ] 實現統計聚合邏輯
- [ ] 實現時間段聚合（7/30/90 天）
- [ ] 實現相關性係數計算
- [ ] 添加 API 緩存機制（避免頻繁計算）
- [ ] 添加單元測試 (TEST-406.1)

### 前端任務（開發者 B）- 6 小時

#### Day 1-2：UI-307.2 星數評分界面
```jsx
// 在練習卡詳細頁面底部

<div className="feedback-section">
  <h3>這個練習卡對你有幫助嗎？</h3>

  {/* 星數評分 */}
  <div className="star-rating">
    {[1,2,3,4,5].map(star => (
      <Star
        key={star}
        filled={userRating >= star}
        onClick={() => setUserRating(star)}
      />
    ))}
  </div>

  {/* 含義顯示 */}
  <p className="meaning">
    {meanings[userRating]}  // "你評分了 4 顆星 - 適用"
  </p>

  {/* 自由文字 */}
  <textarea
    placeholder="補充意見（可選）"
    value={comment}
  />

  {/* 最愛按鈕 */}
  <button
    onClick={() => toggleFavorite()}
    className={isFavorite ? "favorited" : ""}
  >
    ❤️ 加入最愛練習清單
  </button>

  <button onClick={submitFeedback}>提交評分</button>
</div>
```

**檢查清單**：
- [ ] 星數點擊交互
- [ ] 實時顯示星數含義
- [ ] 最愛按鈕獨立於星數
- [ ] 確認訊息顯示
- [ ] 移動設備適配

#### Day 3：UXP-1801 和 UXP-1802（平行進行）

**UXP-1801：進度追蹤卡片**
```jsx
<div className="progress-card">
  <h3>📊 你的進度</h3>
  <div className="stats">
    <Stat
      label="這周練習"
      value={weekCount}
      comparison={`上周 ${lastWeekCount} ↑40%`}
    />
    <Stat
      label="堅持"
      value={`連續 ${streakDays} 天 🔥`}
    />
    <Stat
      label="改善最明顯"
      value="「後坐」"
      change="3★ → 5★"
    />
  </div>
</div>
```

**UXP-1802：推薦理由展示**
```jsx
<div className="recommendation-reason">
  <h4>為什麼推薦這個？</h4>
  <ul>
    <li>✓ 針對你的症狀「後坐」</li>
    <li>✓ 適合你的等級「中級」</li>
    <li>✓ 其他用戶評分 4.6★(28 評)</li>
  </ul>
  <p className="expected-effect">
    預期效果：1-2 周可見改善<br/>
    練習時長：10-15 分鐘/天
  </p>
</div>
```

### 測試任務（QA）- 4 小時

#### 測試覆蓋清單
```javascript
// TEST-406.1：統計端點測試
- 驗證層一、層二統計計算正確
- 驗證時間範圍聚合
- 驗證相關性係數計算
- 驗證大數據集性能

// TEST-406.2：卡片詳情測試
- 驗證星數分布計算
- 驗證改進建議提取
- 驗證 N/A 邊界情況

// UI 界面測試
- 星數點擊交互
- 最愛按鈕獨立性
- 響應式設計
- 安卓/iOS 兼容性
```

### 第 1 周完成檢查清單
- [ ] 所有代碼已提交到 main 分支
- [ ] 單元測試 > 80% 覆蓋率
- [ ] API 文檔已更新
- [ ] 演示環境已部署
- [ ] PM 完成功能驗收

---

## 📋 詳細分解：第 2 周（管理後台）

### 優先順序（推薦同步進行，避免阻塞）

#### 分隊 A：後端分析邏輯（開發者 A+C）- 12 小時
- [ ] API-207.3：症狀有效性分析
- [ ] API-207.4：用戶偏好分析
- [ ] 聚合和緩存優化

#### 分隊 B：前端 UI 頁面（開發者 B+D）- 12 小時
- [ ] UI-308.6：儀表板
- [ ] UI-308.7：卡片詳情頁
- [ ] UI-308.8：症狀分析頁

#### 分隊 C：UX 優化（開發者 E）- 8 小時
- [ ] UXP-1804-1807：P2 優化項目

#### 分隊 D：測試（QA）- 8 小時
- [ ] TEST-406.3-4：集成測試

---

## 💻 開發環境快速啟動

### 1. 數據庫初始化
```bash
# 創建數據庫
createdb turnfix_db

# 運行 migration
alembic upgrade head

# 導入初始症狀和練習卡數據
python scripts/seed_initial_data.py
```

### 2. 後端開發環境
```bash
# 創建虛擬環境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt

# 啟動開發服務器
uvicorn backend.main:app --reload --port 8000
```

### 3. 前端開發環境
```bash
# 安裝依賴
npm install

# 啟動開發服務器
npm run dev

# 訪問 http://localhost:3000
```

### 4. 驗證環境
```bash
# 檢查 API 是否運行
curl http://localhost:8000/api/v1/health

# 檢查數據庫連接
python -c "from backend.db import get_db; print('DB OK')"
```

---

## 📊 進度追蹤表

### 第 1 周進度
| 任務 | 負責人 | 預計 | 實際 | 狀態 | 備註 |
|------|--------|------|------|------|------|
| API-204.3-5 | Dev-A | 4h | - | ⬜ | |
| API-207.1-2 | Dev-A | 4h | - | ⬜ | |
| UI-307.2 | Dev-B | 4h | - | ⬜ | |
| UXP-1801 | Dev-B | 4h | - | ⬜ | |
| UXP-1802 | Dev-B | 2h | - | ⬜ | |
| TEST-406.1-2 | QA | 4h | - | ⬜ | |

---

## 🎯 里程碑定義

### 第 1 周完成 (2025-11-04)
- [ ] 星數反饋系統完全可用
- [ ] API 單元測試通過
- [ ] UI 反饋界面可用
- [ ] P1 UX 優化基本完成

**驗收標準**：
```
✅ 用戶可以給練習卡評分（1-5 顆星）
✅ 用戶可以加入/移除最愛
✅ 首頁顯示進度追蹤卡片
✅ 卡片上顯示推薦理由
✅ 所有 API 端點可正確返回數據
```

### 第 2 周完成 (2025-11-11)
- [ ] 完整管理後台第一期
- [ ] P2 UX 優化完成
- [ ] 集成測試通過

**驗收標準**：
```
✅ 管理員可以看到整體反饋統計
✅ 管理員可以深入分析單張卡片
✅ 用戶體驗明顯改進（快速查詢、視覺反饋等）
✅ 性能指標達標（P95 < 2.5s）
```

### 第 3 周完成 (2025-11-18)
- [ ] 完整管理後台（包括導出）
- [ ] P3 UX 優化完成
- [ ] 回歸測試通過

**驗收標準**：
```
✅ 管理員可以導出數據為 CSV/Excel
✅ 用戶可以設置練習提醒
✅ 連續練習計數器正常工作
✅ 系統性能穩定
```

### 第 4 周完成 (2025-11-25) - 上線
- [ ] P4 UX 優化完成
- [ ] 完整回歸測試通過
- [ ] 安全檢查完成
- [ ] 上線檢查清單全部通過

**驗收標準**：
```
✅ 應用部署到生產環境
✅ 管理員已培訓並準備就緒
✅ 監控告警已配置
✅ 應急計劃已準備
```

---

## 🚨 風險識別與應對

### 風險 1：數據聚合性能
**風險**：管理後台統計計算可能很慢
**應對**：
- 使用數據庫視圖預計算常用統計
- 實現結果緩存（1 小時過期）
- 後台異步任務計算複雜報告

### 風險 2：前後端集成延遲
**風險**：前端等待後端 API 導致進度延迟
**應對**：
- 前端使用 mock API 提前開發
- 后端盡早完成 API 規格文檔
- 前後端並行開發，周一/周四同步點

### 風險 3：數據庫遷移
**風險**：添加新字段可能需要遷移
**應對**：
- 使用 Alembic 管理遷移
- 編寫測試確保遷移正確
- 在演示環境先驗證

---

## 📞 通訊與同步

### 日常同步
- **每天早上 10 點**：15 分鐘站會（進度、障礙）
- **每周一/四下午 3 點**：1 小時設計同步

### 障礙報告
- 遇到無法 24 小時內解決的障礙，立即報告
- 提供：障礙描述、影響範圍、建議解決方案

### 代碼審查
- 所有代碼必須經過至少一人審查
- PR 檢查清單：功能完整、測試覆蓋、無性能回歸

---

## 📚 參考資源

### 關鍵文檔
- `ADMIN_FEEDBACK_ANALYTICS_DESIGN.md` - 完整規格
- `STAR_RATING_QUICK_REFERENCE.md` - API 速查
- `spec/erm.dbml` - 數據庫結構
- `dev-setup.md` - 環境配置

### 技術參考
- FastAPI 文檔：https://fastapi.tiangolo.com/
- React 文檔：https://react.dev/
- SQLAlchemy 文檔：https://docs.sqlalchemy.org/

---

**版本**：v1.0
**最後更新**：2025-10-28
**下一個檢查點**：2025-11-04（第一周完成）

祝開發順利！🚀
