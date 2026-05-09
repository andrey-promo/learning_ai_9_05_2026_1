import logging
import os
import sys

from dotenv import load_dotenv

load_dotenv()


def _require(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        logging.critical("Обязательная переменная окружения не задана: %s", name)
        sys.exit(1)
    return value


class Config:
    def __init__(self) -> None:
        self.telegram_bot_token: str = _require("TELEGRAM_BOT_TOKEN")
        self.openrouter_api_key: str = _require("OPENROUTER_API_KEY")
        self.openrouter_model: str = _require("OPENROUTER_MODEL")
        self.system_prompt: str = _require("SYSTEM_PROMPT")

        self.openrouter_base_url: str = (
            os.getenv("OPENROUTER_BASE_URL", "").strip()
            or "https://openrouter.ai/api/v1"
        )

        raw_temp = os.getenv("LLM_TEMPERATURE", "").strip()
        self.llm_temperature: float = float(raw_temp) if raw_temp else 0.7

        raw_tokens = os.getenv("LLM_MAX_TOKENS", "").strip()
        self.llm_max_tokens: int = int(raw_tokens) if raw_tokens else 1024

        self.log_level: str = os.getenv("LOG_LEVEL", "INFO").strip().upper()

        raw_history = os.getenv("HISTORY_LIMIT", "").strip()
        self.history_limit: int = int(raw_history) if raw_history else 20


def setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
    )
