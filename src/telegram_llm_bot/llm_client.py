import logging

from openai import AsyncOpenAI

from .config import Config

logger = logging.getLogger(__name__)


class LlmClient:
    def __init__(self, config: Config) -> None:
        self._client = AsyncOpenAI(
            api_key=config.openrouter_api_key,
            base_url=config.openrouter_base_url,
        )
        self._model = config.openrouter_model
        self._system_prompt = config.system_prompt
        self._temperature = config.llm_temperature
        self._max_tokens = config.llm_max_tokens

    async def ask(self, user_text: str) -> str:
        response = await self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": self._system_prompt},
                {"role": "user", "content": user_text},
            ],
            temperature=self._temperature,
            max_tokens=self._max_tokens,
        )
        return response.choices[0].message.content or ""
