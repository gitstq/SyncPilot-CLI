# SyncPilot-CLI Makefile
# 轻量级终端智能文件同步与备份引擎构建脚本

.PHONY: help install test clean build lint format

PYTHON := python3
PIP := pip3

help:
	@echo "SyncPilot-CLI - Available Commands:"
	@echo ""
	@echo "  make install    - Install SyncPilot-CLI"
	@echo "  make test       - Run test suite"
	@echo "  make clean      - Clean build artifacts"
	@echo "  make build      - Build distribution packages"
	@echo "  make lint       - Run code linting"
	@echo "  make format     - Format code with black"
	@echo ""

install:
	$(PIP) install -e .

test:
	$(PYTHON) -m pytest tests/ -v --cov=syncpilot --cov-report=term-missing

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	$(PYTHON) setup.py sdist bdist_wheel

lint:
	flake8 syncpilot.py --max-line-length=100
	mypy syncpilot.py --ignore-missing-imports

format:
	black syncpilot.py --line-length=100
