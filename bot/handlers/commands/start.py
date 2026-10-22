from aiogram import F, Router, html
from aiogram.filters import CommandStart
from aiogram.types import Message, User
from aiogram_i18n import I18nContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.user import UserCreate, upsert_user

router = Router(name=__name__)


@router.message(CommandStart(), F.from_user.as_("user"))
async def start_command(message: Message, user: User, i18n: I18nContext, session: AsyncSession) -> None:
    await upsert_user(session, UserCreate(user_id=user.id, username=user.username))
    await message.answer(i18n.get("start", name=html.quote(user.first_name)))
