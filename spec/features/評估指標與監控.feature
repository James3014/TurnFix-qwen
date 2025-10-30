Feature: 評估指標與監控
  作為系統管理員
  我希望能夠追蹤系統的評估指標和效能
  以便了解系統表現並進行改進

  Rule: 追蹤 Helpful Rate
    系統應記錄使用者對提供建議的評分
    
    Example: 計算 Helpful Rate
      Given 系統已運行一段時間
      And 有使用者提供評分
      When 計算 Helpful Rate (👍比率)
      Then 系統應顯示 👍 評分數量佔總評分數量的百分比

  Rule: 追蹤平均追問數
    系統應記錄每次互動的追問次數
    
    Example: 計算平均追問數
      Given 系統已處理多個使用者問題
      When 計算平均追問數
      Then 系統應顯示每次互動的平均追問次數
      And 目標是平均追問數 ≤ 1.0

  Rule: 追蹤 Coverage
    系統應記錄成功映射的比例
    
    Example: 計算 Coverage
      Given 系統已處理多個使用者問題
      When 計算 Coverage (成功映射比例)
      Then 系統應顯示成功辨識並提供練習卡的問題佔總問題數的百分比

  Rule: 系統效能監控
    系統應監控效能指標
    
    Example: 追蹤 API 響應時間
      Given 系統正在運行
      When 監控 API 響應時間
      Then 系統應追蹤 P95 響應時間並確保 < 2.5s

    Example: 追蹤系統可用性
      Given 系統正在運行
      When 監控系統可用性
      Then 系統應追蹤可用性指標