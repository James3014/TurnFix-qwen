# TurnFix 項目 Makefile - 簡化常見開發任務
.PHONY: help install test coverage docker-up clean

help:  ## 顯示幫助信息
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

install:  ## 安裝所有依賴
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

test:  ## 運行所有測試
	cd backend && pytest

coverage:  ## 生成測試覆蓋率報告
	cd backend && pytest --cov=backend --cov-report=term

docker-up:  ## 啟動所有服務
	docker-compose up -d

docker-down:  ## 停止所有服務
	docker-compose down

clean:  ## 清理生成的文件
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
