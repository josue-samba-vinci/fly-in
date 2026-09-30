
PY = uv run python3
MAIN = 
MAP ?= input.txt

install:
	uv sync

run:
	$(PY) $(MAIN) $(MAP)

debug:
	$(PY) -m pdb $(MAIN) $(MAP)

clean:
	rm -rf __pycache__ .mypycache

lint:
	uv run flake8 .
	uv run mypy . --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs
				  --check-untyped-defs

lint-strict:
	uv run flake8 .
	uv run mypy . --strict