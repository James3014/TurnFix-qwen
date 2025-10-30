Feature: 使用者回饋

  Scenario: 收集使用者評分回饋
    Given 系統已提供練習卡
    When 使用者給予評分 "👍"
    Then 系統應記錄此回饋評分

  Scenario: 收集使用者自由文字回饋
    Given 系統已提供練習卡
    When 使用者輸入自由文字回饋 "這些練習很有用，但希望能有更多進階選項"
    Then 系統應記錄此自由文字回饋