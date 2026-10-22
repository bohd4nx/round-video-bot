from aiogram import Bot, Router
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.download import DownloadCreate, add_download
from bot.database.user import UserCreate, upsert_user
from bot.keyboards import OverlayCallback
from bot.services import process_and_send

router = Router(name=__name__)


@router.callback_query(OverlayCallback.filter())
async def overlay_chosen(
    callback: CallbackQuery,
    callback_data: OverlayCallback,
    i18n: I18nContext,
    bot: Bot,
    session: AsyncSession,
) -> None:
    await callback.answer()

    prompt = callback.message
    if not isinstance(prompt, Message):
        return

    video_msg = prompt.reply_to_message
    if video_msg is None or video_msg.video is None:
        # Original video was deleted — nothing to process
        await prompt.delete()
        return

    video = video_msg.video
    await prompt.edit_text(i18n.get("processing"), reply_markup=None)

    ok = await process_and_send(
        file_id=video.file_id,
        video_msg=video_msg,
        status_msg=prompt,
        overlay=callback_data.overlay,
        i18n=i18n,
        bot=bot,
    )
    if not ok:
        return

    user = callback.from_user
    await upsert_user(session, UserCreate(user_id=user.id, username=user.username))
    await add_download(session, DownloadCreate(user_id=user.id, content_type="video_file", content_id=video.file_id))
