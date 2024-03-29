from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

async_engine = create_async_engine(
    str(settings.ASYNC_DATABASE_URL), pool_pre_ping=True, pool_size=10, max_overflow=10
)

async_session_maker = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    id: Any
