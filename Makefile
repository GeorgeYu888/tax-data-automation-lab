.PHONY: install test run clean

install:
	pip install -r requirements.txt

test:
	pytest

run:
	python -m tax_automation_lab run

clean:
	rm -rf outputs .pytest_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +

