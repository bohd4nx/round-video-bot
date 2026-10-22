import asyncio
import logging
import tempfile
from pathlib import Path

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.types import FSInputFile, Message
from aiogram.utils.chat_action import ChatActionSender
from aiogram_i18n import I18nContext

from .video import Overlay, encode_segment, probe, split_segments
from .video.constants import VIDEO_OUTPUT_SIZE

logger = logging.getLogger(__name__)


async def process_and_send(
    file_id: str,
    video_msg: Message,
    status_msg: Message,
    overlay: Overlay,
    i18n: I18nContext,
    bot: Bot,
) -> bool:
    """Download the video, convert it to round notes and reply with them. Returns True on success."""
    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        source = workdir / "source.mp4"

        try:
            await bot.download(file_id, destination=source)
            media = await asyncio.to_thread(probe, source)

            for segment in split_segments(media.duration):
                out_path = workdir / f"segment_{segment.index}.mp4"

                async with ChatActionSender.record_video_note(bot=bot, chat_id=video_msg.chat.id):
                    duration = await asyncio.to_thread(
                        encode_segment, source, out_path, segment, overlay, media.has_audio
                    )

                await video_msg.reply_video_note(
                    FSInputFile(out_path),
                    duration=duration,
                    length=VIDEO_OUTPUT_SIZE,
                )
        except Exception as exc:
            await _report_error(exc, status_msg, i18n)
            return False

    await status_msg.delete()
    return True


async def _report_error(exc: Exception, status_msg: Message, i18n: I18nContext) -> None:
    if isinstance(exc, TelegramAPIError) and "VOICE_MESSAGES_FORBIDDEN" in exc.message:
        await status_msg.edit_text(i18n.get("voice-disabled"))
        return

    logger.error("Failed to process video", exc_info=exc)
    await status_msg.edit_text(i18n.get("error-processing"))
