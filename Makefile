PY = uv run python3
MAIN = map.py
MAP ?= maps/easy/01_linear_path.txt

install:
	uv sync

run:
	$(PY) $(MAIN) $(MAP)

debug:
	$(PY) -m pdb $(MAIN) $(MAP)

clean:
	rm -rf __pycache__ .mypy_cache

lint:
	uv run flake8 .
	uv run mypy . --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 .
	uv run mypy . --strict

.PHONY: install run debug clean lint lint-strict
