from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext

from bot.services.video import Overlay

from .callbacks import OverlayCallback

IOS_EMOJI_ID = "5818920837645867167"
ANDROID_EMOJI_ID = "5819078828017849357"


def overlay_keyboard(i18n: I18nContext) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=i18n.get("btn-ios"),
        icon_custom_emoji_id=IOS_EMOJI_ID,
        callback_data=OverlayCallback(overlay=Overlay.IOS),
    )
    builder.button(
        text=i18n.get("btn-android"),
        icon_custom_emoji_id=ANDROID_EMOJI_ID,
        callback_data=OverlayCallback(overlay=Overlay.ANDROID),
    )
    builder.adjust(1)
    return builder.as_markup()
