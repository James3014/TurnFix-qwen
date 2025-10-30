#!/usr/bin/env python3
"""
TurnFix 開發伺服器啟動腳本

簡單直接，不做過度工程
"""
import uvicorn
import sys
import os

# 添加項目根目錄到 Python 路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("啟動 TurnFix 開發伺服器...")
    print("訪問 http://localhost:8000 查看主頁")
    print("訪問 http://localhost:8000/docs 查看 API 文檔")
    print("按 Ctrl+C 停止伺服器")
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )