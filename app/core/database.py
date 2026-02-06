from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import registry, sessionmaker
from sqlalchemy.inspection import inspect

from app.core.config import settings

mapper_registry = registry()
Base = mapper_registry.generate_base()

engine = create_async_engine(settings.database_url, echo=False)
SessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
    async with SessionLocal() as session:
        yield session


@asynccontextmanager
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
