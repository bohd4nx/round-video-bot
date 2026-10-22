from pathlib import Path
from typing import Any

from aiogram import Dispatcher
from aiogram.types import User
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import BaseCore
from aiogram_i18n.cores.fluent_compile_core import FluentCompileCore
from aiogram_i18n.managers import BaseManager

from bot.core.constants import DEFAULT_LOCALE

LOCALES_PATH = Path(__file__).resolve().parents[2] / "locales" / "{locale}" / "LC_MESSAGES"


class TelegramLocaleManager(BaseManager):
    """Picks the locale from the user's Telegram language; nothing is stored.

    Supported locales are the folders in `locales/`, so adding a language needs no code changes.
    """

    def __init__(self, core: BaseCore[Any]) -> None:
        super().__init__(default_locale=DEFAULT_LOCALE)
        self.core = core

    async def get_locale(self, event_from_user: User | None = None) -> str:
        # Telegram sends IETF tags like "en", "ru" or "pt-br" — only the base language matters
        code = (event_from_user.language_code or "") if event_from_user else ""
        locale = code.split("-")[0].lower()
        return locale if locale in self.core.available_locales else DEFAULT_LOCALE

    async def set_locale(self, locale: str) -> None:
        raise NotImplementedError("Locale follows the user's Telegram language")


def setup_i18n(dp: Dispatcher) -> None:
    core = FluentCompileCore(path=LOCALES_PATH, default_locale=DEFAULT_LOCALE)
    I18nMiddleware(core=core, manager=TelegramLocaleManager(core)).setup(dispatcher=dp)
