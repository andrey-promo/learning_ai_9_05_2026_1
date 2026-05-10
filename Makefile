.PHONY: install run docker-build docker-run

install:
	uv sync

run:
	uv run telegram-llm-bot

docker-build:
	docker build -t telegram-llm-bot .

docker-run:
	docker run --rm --env-file .env telegram-llm-bot
