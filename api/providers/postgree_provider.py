from sqlalchemy.ext.declarative import declarative_base
from core.settings import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession
from fastapi import Request
from typing import AsyncIterator

def make_engine() -> AsyncEngine:
    return create_async_engine(
        settings.DB_CONNECTION_STRING,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
    )


def make_sessionmaker(engine: AsyncEngine) -> AsyncSession:
    return async_sessionmaker(
        engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False
    )

async def get_db(request: Request) -> AsyncIterator[AsyncSession]:
    sessionmaker_ = request.app.state.db_sessionmaker

    async with sessionmaker_() as session:
        yield session

Base = declarative_base()
