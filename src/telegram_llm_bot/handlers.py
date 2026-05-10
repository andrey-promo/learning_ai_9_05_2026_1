import logging
from collections import deque

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from .config import Config
from .llm_client import LlmClient

logger = logging.getLogger(__name__)

router = Router()

_history: dict[int, deque] = {}


def _get_history(user_id: int, limit: int) -> deque:
    if user_id not in _history:
        _history[user_id] = deque(maxlen=limit)
    return _history[user_id]


@router.message(F.chat.type == "private", Command("start"))
async def cmd_start(message: Message) -> None:
    await message.answer(
        "Привет! Я JTBD-консультант на базе языковой модели.\n\n"
        "Помогаю находить продуктовые идеи, формулировать job stories, "
        "выявлять необслуженные работы и желаемые результаты (outcomes).\n\n"
        "Просто напишите, над чем работаете — и начнём."
    )


@router.message(F.chat.type == "private", Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(
        "Я консультирую по методологии Jobs-to-be-Done:\n"
        "• поиск продуктовых идей\n"
        "• job stories и job map\n"
        "• необслуженные работы (underserved jobs)\n"
        "• желаемые результаты (outcomes)\n\n"
        "Напишите текстовое сообщение — я задам уточняющие вопросы "
        "и помогу структурировать мышление."
    )


@router.message(F.chat.type == "private", F.text)
async def handle_text(message: Message, llm_client: LlmClient, config: Config) -> None:
    user_id = message.from_user.id  # type: ignore[union-attr]
    history = _get_history(user_id, config.history_limit)

    try:
        reply = await llm_client.ask(message.text, history=list(history))  # type: ignore[arg-type]
        history.append({"role": "user", "content": message.text})
        history.append({"role": "assistant", "content": reply})
        await message.answer(reply)
    except Exception as exc:
        logger.error("Ошибка при обращении к LLM: %s", exc, exc_info=True)
        await message.answer("Сервис временно недоступен. Попробуйте ещё раз.")


@router.message(F.chat.type == "private", ~F.text)
async def non_text_message(message: Message) -> None:
    await message.answer("Пожалуйста, отправьте текстовое сообщение.")
