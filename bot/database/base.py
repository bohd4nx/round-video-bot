from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from bot.core import config

DATABASE_URL = URL.create(
    "postgresql+asyncpg",
    username=config.postgres_user,
    password=config.postgres_password.get_secret_value(),
    host=config.postgres_host,
    port=config.postgres_port,
    database=config.postgres_db,
)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
)

SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def init_db() -> None:  # used in bot/app.py on startup; in prod prefer alembic migrations
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    await engine.dispose()
