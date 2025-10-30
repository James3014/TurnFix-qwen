# 貢獻指南

感謝您有興趣貢獻 TurnFix 專案！以下是參與開發的指南。

## 開發環境設定

1. 克隆專案：
   ```bash
   git clone <repository-url>
   cd TurnFix
   ```

2. 安裝 Python 依賴：
   ```bash
   pip install -r requirements.txt
   ```

3. 安裝 Node.js 依賴：
   ```bash
   cd frontend
   npm install
   ```

## 分支策略

- `main`：穩定生產版本
- `develop`：開發版本
- `feature/*`：功能開發分支
- `hotfix/*`：緊急修補分支

## 提交規範

請遵循 Conventional Commits 規範：

```
<type>(<scope>): <short summary>
```

常見的 type:
- `feat`: 新功能
- `fix`: 錯誤修復
- `docs`: 文件更新
- `style`: 格式調整
- `refactor`: 重構
- `test`: 測試相關
- `chore`: 構建過程或輔助工具的變動

## 程式碼風格

- Python：遵循 PEP 8 標準
- JavaScript/TypeScript：使用 ESLint 和 Prettier

## 測試

所有功能提交前請確保：
- 單元測試通過
- 整合測試通過
- 沒有新的錯誤或警告

## 問題報告

提交 Issue 時，請提供：
1. 問題描述
2. 重現步驟
3. 預期行為
4. 實際行為
5. 環境資訊（作業系統、瀏覽器等）