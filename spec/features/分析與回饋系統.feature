Feature: 分析與回饋系統
  作為系統管理員
  我希望能夠收集和分析使用者行為及系統效能數據
  以便持續改進系統功能和使用者體驗

  Rule: 使用者行為分析
    系統應追蹤使用者行為數據
    
    Example: 追蹤症狀描述
      Given 使用者輸入症狀描述 "轉彎會後坐"
      When 系統處理該輸入
      Then 系統應記錄此症狀描述的出現頻率和上下文

    Example: 分析練習卡選擇
      Given 使用者獲得練習卡建議並選擇其中一張
      When 使用者選擇特定練習卡
      Then 系統應記錄此選擇並與症狀進行關聯分析

    Example: 追蹤使用者評價
      Given 使用者對練習卡給予評價 👍 或 👎
      When 使用者提交評價
      Then 系統應記錄此評價並關聯到相應的練習卡和症狀

  Rule: 系統效能監控
    系統應監控技術效能指標
    
    Example: API 響應時間監控
      Given 使用者發出 API 請求
      When 系統處理 API 請求
      Then 系統應記錄響應時間並確保 P95 < 2.5s

    Example: 系統可用性監控
      Given 系統正在運行
      When 檢查系統狀態
      Then 系統應報告可用性指標

    Example: 資源使用率監控
      Given 系統正在運行
      When 監控資源使用情況
      Then 系統應報告 CPU、記憶體等資源使用率

  Rule: 回饋收集與分析
    系統應收集並分析使用者回饋
    
    Example: 收集自由文字回饋
      Given 使用者提供自由文字回饋
      When 使用者提交回饋
      Then 系統應記錄此回饋內容

    Example: 分析回饋內容
      Given 系統收集了多個使用者回饋
      When 分析回饋內容
      Then 系統應識別常見問題和改進建議

    Example: 追蹤回饋處理狀態
      Given 系統標記了回饋項目進行處理
      When 管理員處理回饋
      Then 系統應更新回饋處理狀態並通知相關人員