# TurnFix 開發 Makefile
# 簡單直接，不做過度工程

.PHONY: help install dev-install run test lint format clean

help:
	@echo "TurnFix 開發命令:"
	@echo "  make install      - 安裝生產依賴"
	@echo "  make dev-install  - 安裝開發依賴"
	@echo "  make run          - 啟動開發伺服器"
	@echo "  make test         - 運行測試"
	@echo "  make lint         - 代碼風格檢查"
	@echo "  make format       - 格式化代碼"
	@echo "  make clean        - 清理臨時文件"

install:
	pip install -r requirements.txt

dev-install: install
	pip install -r requirements-dev.txt

run:
	python start_dev_server.py

test:
	pytest tests/ -v

lint:
	flake8 backend/ tests/
	mypy backend/ tests/

format:
	black backend/ tests/

clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -exec rm -f {} +

# 組合命令
dev: dev-install run

check: lint test