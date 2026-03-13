from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

# Асинхронный движок для FastAPI
async_engine = create_async_engine(url=settings.database_url_async, echo=False)
async_session_maker = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

# Синхронный движок для Celery
sync_engine = create_engine(url=settings.database_url_sync, pool_pre_ping=True)
sync_session_maker = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

async def get_async_session():
    async with async_session_maker() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


def get_sync_session():
    with sync_session_maker() as session:
        yield session