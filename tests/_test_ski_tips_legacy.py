"""
滑雪技巧建議服務測試

簡單測試，不做過度工程
保持與簡化實現的兼容性
"""
import pytest
from backend.services.simple_ski_tips import get_ski_tips, identify_symptom, filter_cards_by_conditions, rank_cards

def test_basic_functionality():
    """測試基本功能"""
    result = get_ski_tips("轉彎會後坐")
    assert isinstance(result, list)
    assert len(result) > 0

def test_symptom_identification():
    """測試症狀識別"""
    symptom = identify_symptom("轉彎會後坐")
    assert "id" in symptom
    assert "name" in symptom
    assert symptom["name"] == "重心太後"

def test_filtering_with_conditions():
    """測試條件篩選"""
    # 模擬一些練習卡
    mock_cards = [
        {
            "id": 1,
            "name": "測試卡片",
            "level": ["初級"],
            "terrain": ["綠線"]
        }
    ]
    
    # 測試篩選功能
    result = filter_cards_by_conditions(mock_cards, "初級", "綠線", None)
    assert isinstance(result, list)

def test_ranking():
    """測試排序功能"""
    mock_cards = [
        {
            "id": 1,
            "name": "卡片1"
        },
        {
            "id": 2,
            "name": "卡片2"
        }
    ]
    
    result = rank_cards(mock_cards, None, None)
    assert len(result) == 2

def test_edge_cases():
    """測試邊緣情況"""
    # 空輸入
    result = get_ski_tips("")
    assert isinstance(result, list)
    
    # 特殊字符
    result = get_ski_tips("!@#$%^&*()")
    assert isinstance(result, list)

def test_api_compatibility():
    """測試 API 兼容性"""
    from backend.services.simple_ski_tips import process_ski_tips_request
    
    result = process_ski_tips_request("轉彎會後坐", level="初級", terrain="綠線")
    assert "status" in result
    assert "recommended_cards" in result
    assert "count" in result
    assert result["status"] == "success"

if __name__ == "__main__":
    pytest.main([__file__])