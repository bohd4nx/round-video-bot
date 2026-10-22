import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.core import config, setup_logging
from bot.database import close_db, init_db
from bot.handlers import router
from bot.middlewares import DatabaseMiddleware, setup_i18n

logger = logging.getLogger(__name__)


def create_bot() -> Bot:
    return Bot(
        token=config.bot_token.get_secret_value(),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview_is_disabled=True,
        ),
    )


def create_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    dp.include_router(router)

    setup_i18n(dp)
    dp.update.outer_middleware(DatabaseMiddleware())

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    return dp


async def on_startup() -> None:
    await init_db()
    logger.info("Bot started")


async def on_shutdown() -> None:
    await close_db()


async def run() -> None:
    setup_logging()

    bot = create_bot()
    dp = create_dispatcher()

    await dp.start_polling(
        bot,
        polling_timeout=30,
        handle_as_tasks=True,
        tasks_concurrency_limit=100,
        close_bot_session=True,
    )
