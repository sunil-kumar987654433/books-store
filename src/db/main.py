from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession
from sqlmodel import SQLModel, text, create_engine
from src.config import Config
from typing import Annotated, AsyncGenerator
from fastapi import Depends


engine  = create_async_engine(
        url=Config.DATABASE_URL
    )


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session()->AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]