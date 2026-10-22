from aiogram import F, Router
from aiogram.types import Message, Video
from aiogram_i18n import I18nContext

from bot.core.constants import MAX_FILE_SIZE_BYTES
from bot.keyboards import overlay_keyboard

router = Router(name=__name__)


@router.message(F.video.as_("video"))
async def video_received(message: Message, video: Video, i18n: I18nContext) -> None:
    size = video.file_size or 0
    if size > MAX_FILE_SIZE_BYTES:
        await message.reply(i18n.get("error-file-too-large", size=round(size / (1024 * 1024), 1)))
        return

    # The prompt replies to the video, so the callback can find it via reply_to_message
    await message.reply(
        i18n.get("overlay-choose"),
        reply_markup=overlay_keyboard(i18n),
    )
