# 貢獻指南

感謝你考慮為 TurnFix 項目做出貢獻！這份文檔將指導你如何參與這個項目。

## 行為準則

### 我們的承諾

為了營造一個開放和友好的環境，我們作為貢獻者和維護者承諾：讓每個人參與我們的項目和社區時都能獲得無騷擾的體驗。

### 我們的標準

積極行為的例子包括：

* 使用友好和包容的語言
* 尊重不同的觀點和經驗
* 優雅地接受建設性批評
* 關注什麼對社區最有利
* 對其他社區成員表示同理心

## 如何貢獻

### 報告 Bug

在提交 bug 報告之前，請檢查 [Issues](https://github.com/yourusername/TurnFix-qwen/issues) 確保該問題尚未被報告。

提交 bug 時，請包含：

- **清晰的標題和描述**
- **重現步驟**
- **預期行為** vs **實際行為**
- **環境信息**（操作系統、Python/Node 版本等）
- **相關日誌或錯誤信息**

### 建議新功能

功能請求應該在 Issues 中提出。請清楚說明：

- **功能的目的和動機**
- **期望的行為**
- **可能的實現方案**（如果有想法）

### 提交代碼

#### 準備工作

1. Fork 本倉庫
2. 克隆你的 fork：
   ```bash
   git clone https://github.com/YOUR-USERNAME/TurnFix-qwen.git
   cd TurnFix-qwen
   ```

3. 添加上游倉庫：
   ```bash
   git remote add upstream https://github.com/ORIGINAL-OWNER/TurnFix-qwen.git
   ```

4. 創建新分支：
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### 開發流程

1. **設置開發環境**

   後端：
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

   前端：
   ```bash
   cd frontend
   npm install
   ```

2. **進行更改**

   - 遵循現有的代碼風格
   - 保持函數簡潔（<50 行）
   - 組件不超過 150 行
   - 添加必要的註釋

3. **編寫測試**

   - 為新功能添加測試
   - 確保所有測試通過：
     ```bash
     # 後端
     cd backend
     pytest

     # 前端
     cd frontend
     npm test
     ```

4. **檢查代碼覆蓋率**

   ```bash
   pytest --cov=backend --cov-report=term-missing
   ```

   確保覆蓋率不降低。

5. **運行代碼格式化**

   ```bash
   # Python (如果安裝了 black)
   black backend/

   # JavaScript (如果配置了 prettier)
   npm run format
   ```

#### 提交規範

我們使用 [Conventional Commits](https://www.conventionalcommits.org/) 規範：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**類型 (type)**：

- `feat`: 新功能
- `fix`: Bug 修復
- `docs`: 文檔更新
- `style`: 代碼格式調整（不影響功能）
- `refactor`: 重構
- `test`: 測試相關
- `chore`: 構建工具或輔助工具的變動

**範例**：

```
feat(api): 添加用戶認證端點

- 實現 JWT token 生成
- 添加登錄和註冊路由
- 包含 bcrypt 密碼哈希

Closes #123
```

#### Pull Request 流程

1. **更新你的分支**

   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **推送到你的 fork**

   ```bash
   git push origin feature/your-feature-name
   ```

3. **創建 Pull Request**

   在 GitHub 上打開 PR，填寫 PR 模板：

   - 描述你的更改
   - 關聯相關的 Issue
   - 列出測試計劃
   - 添加截圖（如果是 UI 更改）

4. **代碼審查**

   - 回應審查意見
   - 根據反饋進行修改
   - 保持討論專業和友好

5. **合併**

   一旦 PR 被批准且所有檢查通過，維護者會合併你的更改。

### 開發檢查清單

提交 PR 前，請確保：

- [ ] 代碼遵循項目風格指南
- [ ] 所有測試通過
- [ ] 添加了新功能的測試
- [ ] 代碼覆蓋率沒有降低
- [ ] 更新了相關文檔
- [ ] Commit 消息遵循規範
- [ ] 沒有遺留的 console.log 或調試代碼
- [ ] 沒有合併衝突

## 代碼風格指南

### Python (後端)

遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 和 Linus 的"好品味"原則：

- 使用 4 空格縮進
- 每行不超過 88 字符
- 函數名使用 snake_case
- 類名使用 PascalCase
- 常量使用 UPPER_CASE
- 優先簡潔而非聰明的代碼

**好例子**：

```python
def get_ski_tips(db: Session, user_input: str) -> List[Dict]:
    """獲取滑雪建議 - 簡單直接"""
    symptom = identify_symptom(user_input)
    cards = get_practice_cards(symptom.id)
    return [card_to_dict(card) for card in cards]
```

**壞例子**：

```python
def get_ski_tips_advanced_with_caching_and_filtering(
    db, input, level=None, terrain=None, style=None,
    cache_enabled=True, filter_by_user_history=False
):
    # 過度工程化...
```

### JavaScript/React (前端)

- 使用 2 空格縮進
- 使用函數組件和 Hooks
- 組件名使用 PascalCase
- 文件名與組件名一致
- Props 解構在函數簽名中
- 優先組合而非繼承

**好例子**：

```javascript
export function PracticeCard({ card, onFeedback }) {
  return (
    <div className="card">
      <h3>{card.name}</h3>
      <p>{card.goal}</p>
      <button onClick={() => onFeedback(card.id)}>
        反饋
      </button>
    </div>
  );
}
```

## 文檔

### 代碼註釋

- 解釋「為什麼」而不是「什麼」
- 複雜邏輯需要註釋
- API 端點需要 docstring
- 公開函數需要參數和返回值說明

### 文檔更新

如果你的 PR 改變了：

- **API 端點** → 更新 API 文檔
- **配置選項** → 更新 README.md
- **安裝步驟** → 更新快速開始指南
- **新功能** → 添加使用範例

## 測試指南

### 測試類型

1. **單元測試**：測試獨立函數和類
2. **集成測試**：測試 API 端點
3. **端到端測試**：測試完整用戶流程

### 測試命名

```python
def test_<function>_<scenario>_<expected_result>():
    # 範例
    def test_identify_symptom_by_synonym_returns_correct_symptom():
        pass
```

### 測試結構

遵循 AAA 模式：

```python
def test_create_symptom_success():
    # Arrange（準備）
    symptom_data = {"name": "重心太後", "category": "技術"}

    # Act（執行）
    result = create_symptom(symptom_data)

    # Assert（驗證）
    assert result.id is not None
    assert result.name == "重心太後"
```

## 版本發布

版本號遵循 [Semantic Versioning](https://semver.org/):

- **MAJOR**: 不兼容的 API 更改
- **MINOR**: 向後兼容的功能添加
- **PATCH**: 向後兼容的 bug 修復

## 獲取幫助

- 查看 [README.md](./README.md) 了解項目概況
- 瀏覽 [Issues](https://github.com/yourusername/TurnFix-qwen/issues) 查看已知問題
- 加入討論 [Discussions](https://github.com/yourusername/TurnFix-qwen/discussions)

## 致謝

感謝所有為這個項目做出貢獻的人！

每一個 PR、Issue 報告、文檔改進都讓這個項目變得更好。

---

再次感謝你的貢獻！🎿
