import asyncio
import logging

from aiogram import Bot, Dispatcher

from .config import Config, setup_logging
from .handlers import router

logger = logging.getLogger(__name__)


async def _run() -> None:
    config = Config()
    setup_logging(config.log_level)

    bot = Bot(token=config.telegram_bot_token)
    dp = Dispatcher()
    dp.include_router(router)

    logger.info("Бот запускается, начинаем long polling")
    try:
        await dp.start_polling(bot)
    finally:
        logger.info("Polling остановлен, закрываем сессию бота")
        await bot.session.close()


def main() -> None:
    asyncio.run(_run())


if __name__ == "__main__":
    main()
