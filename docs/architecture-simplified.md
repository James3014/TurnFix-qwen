# TurnFix 簡化架構設計

根據 Linus Torvalds 的"好品味"原則，我們對 TurnFix 系統進行了架構簡化：

## 1. 核心原則

### 1.1 消除不必要的複雜度
- 移除多代理架構，使用簡單函數實現核心邏輯
- 保持資料模型不變，但簡化實現層
- 保留 RAG 架構但簡化調用方式

### 1.2 保持實現簡單直接
- 使用函數而非複雜物件導向設計
- 保持數據流簡單清晰
- 專注於解決核心問題

### 1.3 確保向後兼容性
- 保持 API 接口不變
- 保持數據格式一致
- 保持配置文件兼容

## 2. 簡化後架構

```
┌─────────────────────────────────────────────────────────────────┐
│                        前端 (React + TypeScript)                │
├─────────────────────────────────────────────────────────────────┤
│  UI Components → State Management → API Clients                 │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                        後端 (FastAPI)                           │
├─────────────────────────────────────────────────────────────────┤
│  API Routes → Service Functions → RAG/LLM Integration           │
│                                │                                │
│                                ▼                                │
│                    ┌─────────────────────────┐                  │
│                    │   AI/LLM Layer          │                  │
│                    │  (RAG + Generation)     │                  │
│                    └─────────────────────────┘                  │
└─────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
        ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
        │   SQLite DB     │ │ Chroma Vector   │ │ External APIs   │
        │   (ORM:         │ │ DB              │ │ (LLM, etc)      │
        │   SQLAlchemy)   │ │ (Embeddings)    │ │                 │
        └─────────────────┘ └─────────────────┘ └─────────────────┘
```

## 3. 實現層簡化

### 3.1 服務層簡化
```python
# 簡化前：多代理架構
class SymptomAnalyzerAgent:
    def process(self, data: TurnFixData) -> TurnFixData:
        # 複雜的代理調用鏈

# 簡化後：簡單函數
def identify_symptom(user_input: str) -> Symptom:
    """
    使用 AI 進行語義匹配，但返回預定義的症狀實體
    """
    # 1. 向量化使用者輸入
    user_vector = embed_sentence(user_input)
    
    # 2. 在 Symptom 向量庫中搜尋最相似的症狀
    similar_symptoms = search_similar_symptoms(user_vector, threshold=0.7)
    
    # 3. 返回最匹配的症狀或觸發追問機制
    if len(similar_symptoms) == 1:
        return similar_symptoms[0]
    elif len(similar_symptoms) > 1:
        # 觸發追問機制
        return trigger_follow_up_questions(similar_symptoms)
    else:
        # 返回安全基礎練習組
        return get_safe_practice_set()
```

### 3.2 數據模型簡化
```python
# 簡化前：複雜的 Pydantic 模型
class SymptomModel(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(max_length=100)
    synonyms: List[str] = Field(default_factory=list)
    # ... 複雜的驗證邏輯

# 簡化後：簡單的字典結構
def create_symptom_dict(
    id: int,
    name: str,
    synonyms: List[str] = None,
    level_scope: List[str] = None,
    terrain_scope: List[str] = None,
    style_scope: List[str] = None,
    category: str = "技術"
) -> Dict[str, Any]:
    """
    創建簡單的症狀字典結構
    """
    return {
        "id": id,
        "name": name,
        "synonyms": synonyms or [],
        "level_scope": level_scope or [],
        "terrain_scope": terrain_scope or [],
        "style_scope": style_scope or [],
        "category": category
    }
```

### 3.3 API 層簡化
```python
# 簡化前：複雜的路由處理
@router.post("/ski-tips", tags=["ski-tips"])
async def get_ski_tips_endpoint(complex_request: ComplexRequestModel):
    # 多層代理調用

# 簡化後：簡單的路由處理
@router.post("/ski-tips", tags=["ski-tips"])
async def get_ski_tips_endpoint(
    input_text: str = Query(...),
    level: Optional[str] = Query(None),
    terrain: Optional[str] = Query(None),
    style: Optional[str] = Query(None)
):
    """
    獲取滑雪技巧建議的簡單路由
    """
    # 直接調用服務函數
    tips = get_ski_recommendations(input_text, level, terrain, style)
    return {
        "status": "success",
        "recommended_cards": tips,
        "count": len(tips)
    }
```

## 4. 保持的核心功能

### 4.1 RAG 架構保持不變
- 知識來源：教練文字答覆/Q&A + 影片逐字稿
- 預處理：清洗、分段、結構化、向量化
- 儲存：ChromaDB 向量資料庫
- 檢索：根據使用者問題檢索相關知識片段
- 選擇：根據檢索結果和使用者條件選擇最適合的練習卡

### 4.2 AI 能力保持不變
- 語義理解：處理口語問題到標準症狀的映射
- 同義詞處理：識別不同表達的同一症狀
- 個性化推薦：根據使用者條件調整練習建議
- 知識檢索：從教練知識庫中找到相關練習

### 4.3 數據模型保持不變
- Symptom：症狀實體保持不變
- PracticeCard：練習卡實體保持不變
- Session：會話實體保持不變
- SymptomPracticeMapping：症狀練習卡映射關係保持不變

## 5. 簡化帶來的好處

### 5.1 開發效率提升
- 減少調試複雜度
- 降低學習曲線
- 提高代碼可讀性

### 5.2 性能優化
- 減少對象創建開銷
- 簡化數據處理流程
- 提升響應速度

### 5.3 維護性改善
- 降低維護複雜度
- 提高代碼可維護性
- 減少技術債務

### 5.4 兼容性保障
- 保持 API 接口不變
- 保持數據格式一致
- 保持配置文件兼容

## 6. 實施步驟

### 6.1 第一階段：服務層簡化
1. 移除多代理架構
2. 使用簡單函數實現核心邏輯
3. 保持與現有 API 接口兼容

### 6.2 第二階段：數據模型簡化
1. 使用字典結構替代複雜 Pydantic 模型
2. 保持資料庫 schema 不變
3. 確保數據處理一致性

### 6.3 第三階段：API 層簡化
1. 簡化路由處理邏輯
2. 保持接口不變
3. 測試兼容性

### 6.4 第四階段：驗證與部署
1. 全面測試確保功能不變
2. 性能基準測試
3. 部署到生產環境

## 7. 風險控制

### 7.1 降級策略
- 在服務層實現降級策略
- 提供默認數據處理
- 確保系統穩定性

### 7.2 錯誤處理
- 保持現有錯誤處理機制
- 添加必要的錯誤日誌
- 確保錯誤可追溯

### 7.3 監控機制
- 保持現有監控機制
- 添加性能指標監控
- 確保問題可及時發現

這樣的簡化架構既保持了 TurnFix 系統的核心功能，又大大降低了實現的複雜度，符合 Linus Torvalds 的"好品味"原則。