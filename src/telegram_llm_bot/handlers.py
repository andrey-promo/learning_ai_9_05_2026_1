from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(F.chat.type == "private", Command("start"))
async def cmd_start(message: Message) -> None:
    await message.answer(
        "Привет! Я бот на базе языковой модели.\n"
        "Просто напишите мне любое сообщение — и я отвечу."
    )


@router.message(F.chat.type == "private", Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(
        "Напишите мне текстовое сообщение, и я передам его языковой модели и пришлю ответ."
    )


@router.message(F.chat.type == "private", ~F.text)
async def non_text_message(message: Message) -> None:
    await message.answer("Пожалуйста, отправьте текстовое сообщение.")
