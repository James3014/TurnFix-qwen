"""
視頻示範鏈接服務

實現 UXP-1815 功能：視頻示範鏈接
"""
from typing import List, Dict, Optional
from urllib.parse import quote
import requests
import re


def extract_keywords_from_practice_card(card_name: str, card_goal: str) -> List[str]:
    """
    從練習卡名稱和目標中提取關鍵字
    """
    keywords = []
    
    # 提取練習卡名稱中的關鍵詞
    if card_name:
        keywords.extend(re.findall(r'\w+', card_name.lower()))
    
    # 提取練習卡目標中的關鍵詞
    if card_goal:
        keywords.extend(re.findall(r'\w+', card_goal.lower()))
    
    # 去除重複和過短的詞
    keywords = list(set([kw for kw in keywords if len(kw) > 2]))
    
    # 添加一些通用的滑雪術語
    keywords.extend(['ski', '滑雪', 'turn', '轉彎', 'technique', '技巧'])
    
    return keywords


def search_youtube_videos(card_name: str, card_goal: str, api_key: str) -> List[Dict[str, str]]:
    """
    搜索與練習卡相關的 YouTube 視頻
    """
    keywords = extract_keywords_from_practice_card(card_name, card_goal)
    
    # 使用前幾個關鍵詞進行搜索
    search_query = ' '.join(keywords[:3]) + ' skiing tutorial'
    
    search_url = f"https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'q': search_query,
        'type': 'video',
        'maxResults': 5,
        'key': api_key
    }
    
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        videos = []
        for item in data.get('items', []):
            video = {
                'id': item['id']['videoId'],
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'thumbnail': item['snippet']['thumbnails']['default']['url'],
                'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            }
            videos.append(video)
        
        return videos
    except Exception as e:
        print(f"搜索 YouTube 視頻時出錯: {e}")
        return []


def get_video_suggestions(card_name: str, card_goal: str, api_key: Optional[str] = None) -> List[Dict[str, str]]:
    """
    獲取練習卡的視頻示範建議
    """
    # 如果沒有提供 API 金鑰，返回空列表
    if not api_key:
        return []
    
    return search_youtube_videos(card_name, card_goal, api_key)