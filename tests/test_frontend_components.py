"""
前端組件測試 (UI-300到UI-309)

測試所有前端組件的功能
"""
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

@pytest.fixture(scope="module")
def browser():
    """創建瀏覽器實例"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 無頭模式
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()

def test_home_page(browser):
    """測試首頁功能 (UI-300)"""
    # 訪問首頁
    browser.get("http://localhost:3000/")
    
    # 驗證頁面標題
    assert "TurnFix" in browser.title
    
    # 驗證導航菜單
    nav_menu = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "navigation"))
    )
    assert nav_menu is not None
    
    # 驗證CTA按鈕
    cta_button = browser.find_element(By.CLASS_NAME, "cta-button")
    assert cta_button is not None
    assert cta_button.text == "開始診斷"

def test_user_input_interface(browser):
    """測試使用者輸入介面 (UI-301)"""
    # 訪問輸入頁面
    browser.get("http://localhost:3000/input")
    
    # 驗證頁面元素
    header = browser.find_element(By.TAG_NAME, "h1")
    assert "描述您的滑行困難" in header.text
    
    # 驗證輸入框
    text_area = browser.find_element(By.ID, "problem-description")
    assert text_area is not None
    
    # 驗證選填資訊
    optional_section = browser.find_element(By.CLASS_NAME, "optional-section")
    assert optional_section is not None
    
    # 驗證提交按鈕
    submit_button = browser.find_element(By.CLASS_NAME, "submit-button")
    assert submit_button is not None
    assert submit_button.text == "獲取練習建議"

def test_adaptive_followup_interface(browser):
    """測試自適應追問介面 (UI-302)"""
    # 訪問追問頁面
    browser.get("http://localhost:3000/followup")
    
    # 驗證頁面元素
    header = browser.find_element(By.TAG_NAME, "h1")
    assert "自適應追問" in header.text
    
    # 驗證追問問題區域
    questions_section = browser.find_element(By.CLASS_NAME, "questions-section")
    assert questions_section is not None
    
    # 驗證提交按鈕
    submit_button = browser.find_element(By.CLASS_NAME, "submit-button")
    assert submit_button is not None

def test_practice_card_display(browser):
    """測試練習卡展示介面 (UI-303)"""
    # 訪問結果頁面
    browser.get("http://localhost:3000/results")
    
    # 驗證頁面元素
    header = browser.find_element(By.TAG_NAME, "h1")
    assert "滑雪練習建議" in header.text
    
    # 驗證練習卡列表
    cards_grid = browser.find_element(By.CLASS_NAME, "cards-grid")
    assert cards_grid is not None
    
    # 驗證練習卡數量提示
    count_message = browser.find_element(By.CLASS_NAME, "count-message")
    assert count_message is not None

def test_practice_card_detail(browser):
    """測試練習卡詳細頁面 (UI-304)"""
    # 訪問練習卡詳細頁面
    browser.get("http://localhost:3000/practice-card/1")
    
    # 驗證頁面元素
    card_title = browser.find_element(By.TAG_NAME, "h1")
    assert card_title is not None
    
    # 驗證練習卡內容
    card_body = browser.find_element(By.CLASS_NAME, "card-body")
    assert card_body is not None
    
    # 驗證練習要點
    tips_section = browser.find_element(By.XPATH, "//h3[text()='練習要點']")
    assert tips_section is not None
    
    # 驗證自我檢查點
    self_check_section = browser.find_element(By.XPATH, "//h3[text()='自我檢查點']")
    assert self_check_section is not None

def test_practice_history(browser):
    """測試練習歷史頁面 (UI-305)"""
    # 訪問歷史頁面
    browser.get("http://localhost:3000/history")
    
    # 驗證頁面元素
    header = browser.find_element(By.TAG_NAME, "h1")
    assert "練習歷史" in header.text
    
    # 驗證歷史記錄列表
    history_list = browser.find_element(By.CLASS_NAME, "history-list")
    assert history_list is not None
    
    # 驗證篩選功能
    filter_section = browser.find_element(By.CLASS_NAME, "filter-section")
    assert filter_section is not None

def test_settings_page(browser):
    """測試設定頁面 (UI-306)"""
    # 訪問設定頁面
    browser.get("http://localhost:3000/settings")
    
    # 驗證頁面元素
    header = browser.find_element(By.TAG_NAME, "h1")
    assert "設定" in header.text
    
    # 驗證設定選項
    settings_form = browser.find_element(By.CLASS_NAME, "settings-form")
    assert settings_form is not None
    
    # 驗證保存按鈕
    save_button = browser.find_element(By.CLASS_NAME, "save-button")
    assert save_button is not None

def test_multi_layer_feedback_interface(browser):
    """測試多層回饋介面 (UI-307)"""
    # 訪問回饋頁面
    browser.get("http://localhost:3000/feedback")
    
    # 驗證頁面元素
    header = browser.find_element(By.TAG_NAME, "h1")
    assert "提供回饋" in header.text
    
    # 驗證回饋層級標籤
    feedback_tabs = browser.find_elements(By.CLASS_NAME, "feedback-tab")
    assert len(feedback_tabs) >= 2
    
    # 驗證會話層級回饋
    session_feedback_tab = browser.find_element(By.XPATH, "//button[contains(text(), '會話回饋')]")
    assert session_feedback_tab is not None
    
    # 驗證練習卡層級回饋
    practice_card_feedback_tab = browser.find_element(By.XPATH, "//button[contains(text(), '練習卡回饋')]")
    assert practice_card_feedback_tab is not None

def test_admin_dashboard_interface(browser):
    """測試管理者後台介面 (UI-308)"""
    # 訪問管理後台
    browser.get("http://localhost:3000/admin")
    
    # 驗證頁面元素
    header = browser.find_element(By.TAG_NAME, "h1")
    assert "管理後台" in header.text
    
    # 驗證儀表板
    dashboard = browser.find_element(By.CLASS_NAME, "dashboard")
    assert dashboard is not None
    
    # 驗證導航菜單
    admin_nav = browser.find_element(By.CLASS_NAME, "admin-nav")
    assert admin_nav is not None

def test_favorite_practice_cards_interface(browser):
    """測試最愛練習清單頁面 (UI-309)"""
    # 訪問最愛頁面
    browser.get("http://localhost:3000/favorites")
    
    # 驗證頁面元素
    header = browser.find_element(By.TAG_NAME, "h1")
    assert "最愛練習清單" in header.text
    
    # 驗證最愛列表
    favorites_list = browser.find_element(By.CLASS_NAME, "favorites-list")
    assert favorites_list is not None
    
    # 驗證空狀態處理
    empty_state = browser.find_element(By.CLASS_NAME, "empty-state")
    assert empty_state is not None