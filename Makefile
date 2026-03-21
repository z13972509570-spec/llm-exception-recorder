.PHONY: install test

install:
	pip install -e .

test:
	pytest tests/ -v

run:
	llm-err stat
	llm-err list
