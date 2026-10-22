from aiogram.filters.callback_data import CallbackData

from bot.services.video import Overlay


class OverlayCallback(CallbackData, prefix="overlay"):
    overlay: Overlay
