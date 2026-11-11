.PHONY: install data analysis register test all clean

install:
	python -m pip install -e ".[dev]"

data:
	python -m sfa_fairness.generate_data

analysis:
	python -m sfa_fairness.pipeline

register:
	python scripts/build_risk_register.py

test:
	pytest -q

all: data analysis register test

clean:
	rm -rf results/figures/*.png results/tables/*.csv results/metrics_summary.json .pytest_cache
