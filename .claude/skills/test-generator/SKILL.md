# Test Generator Skill

## 🎯 名稱
test-generator

## 📝 描述
根據 TurnFix API 規格、UI 設計和任務分解，自動生成符合 TDD 規範的單元測試、集成測試和 UI 測試代碼。支持後端 (pytest) 和前端 (Jest) 測試生成。

## 🎨 功能

### 後端測試生成
- ✅ 根據 API-2xx 規格生成 pytest 單元測試
- ✅ 生成 API 端點測試（含請求/響應驗證）
- ✅ 生成業務邏輯層測試
- ✅ 生成數據層測試
- ✅ 支持 Mock 和 Fixture 生成
- ✅ 支持參數化測試（多個輸入場景）

### 前端測試生成
- ✅ 根據 UI-3xx 設計生成 Jest/React Testing Library 測試
- ✅ 生成組件交互測試
- ✅ 生成渲染測試
- ✅ 生成集成測試
- ✅ 支持 Mock API 調用

### 測試套件生成
- ✅ 生成完整的功能測試套件（如 TEST-406）
- ✅ 生成邊界情況和異常測試
- ✅ 生成性能測試
- ✅ 遵循 Given-When-Then 模式
- ✅ 包含詳細的測試註釋

## 💻 使用方式

### 基本用法

```
"為 API-204.3 生成 pytest 測試代碼"
```

### 進階用法

```
"為 UI-307.2 星數評分組件生成 Jest 測試，包括交互測試"

"為 API-207.1 反饋統計端點生成完整的測試套件，包括邊界情況"

"根據 TEST-406 的測試計劃為管理後台生成所有測試代碼"

"生成 UXP-1801 進度追蹤功能的測試（包括進度計算邏輯測試）"

"為整個反饋系統（API-204 到 API-207）生成完整的集成測試"
```

## 📋 輸出格式

### 後端測試（pytest）
```python
import pytest
from backend.api.feedback import submit_feedback

class TestPracticeCardFeedback:
    """測試類"""

    def test_should_save_star_rating_correctly(self, client, test_db):
        """測試案例名稱清晰，遵循 Given-When-Then"""
        # Given - 前置條件
        # When - 執行操作
        # Then - 驗證結果
        assert result == expected
```

### 前端測試（Jest）
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { StarRating } from '@/components/StarRating';

describe('StarRating Component', () => {
  it('should display 5 stars', () => {
    // 使用 React Testing Library 最佳實踐
    // 關注用戶行為而非實現細節
  });
});
```

## 🎯 生成時的最佳實踐

✅ **必須遵循**：
- 遵循項目的 TDD 規範（見 TDD_AUTOMATION_GUIDE.md）
- 使用有意義的測試名稱（`test_should_*` 模式）
- 一個測試只測一件事
- Mock 外部依賴（數據庫、API 等）
- 包含邊界情況測試
- 目標覆蓋率 ≥ 80%

❌ **應避免**：
- 多個測試用例在一個函數中
- 過度 Mock（應該真實集成測試重要路徑）
- 跳過異常和邊界情況
- 測試實現細節而非行為

## 🔗 相關參考文件

- **TDD_AUTOMATION_GUIDE.md** - TDD 規範和最佳實踐
- **TDD_QUICK_START.md** - 快速開始指南
- **tasks.md** - 完整的任務分解（包含 TEST-4xx）
- **ADMIN_FEEDBACK_ANALYTICS_DESIGN.md** - API 詳細規格
- **STAR_RATING_FEEDBACK_DESIGN.md** - 星數系統設計

## 📊 支持的任務類型

| 任務代碼 | 測試類型 | 複雜度 |
|---------|---------|--------|
| API-20x | 單元測試 + 集成測試 | ⭐⭐⭐ |
| UI-30x | 組件測試 + E2E | ⭐⭐ |
| TEST-40x | 完整測試套件 | ⭐⭐⭐⭐ |
| UXP-18xx | 功能測試 | ⭐⭐ |

## 🚀 工作流程整合

使用本 Skill 支持 TDD 工作流：

1. **紅色階段** 🔴：使用本 Skill 生成測試
2. **綠色階段** 🟢：根據生成的測試寫實現代碼
3. **藍色階段** 🔵：重構代碼，確保測試仍通過

## 🔑 關鍵特性

- 🎯 **快速生成**：5 分鐘內生成完整的功能測試套件
- 📚 **文檔詳細**：每個測試都有註釋說明
- ✅ **TDD 友好**：生成的測試符合 TDD 規範
- 🔄 **可維護**：清晰的結構，易於修改擴展
- 🛡️ **高質量**：覆蓋邊界情況和異常流程

## 💡 範例請求

```
"TurnFix 項目中，為 API-207.1（反饋統計）生成完整的測試代碼。
應該包括：
1. 測試層一統計計算正確
2. 測試層二統計計算正確
3. 測試相關性係數計算
4. 測試趨勢數據
使用 pytest，遵循 TDD 規範"
```

---

**版本**：v1.0
**維護者**：TurnFix 開發團隊
**更新日期**：2025-10-28
