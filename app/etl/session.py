"""
Sessão SQLAlchemy para ETL.

O ETL usa a mesma sessão async da API (AsyncSession) para poder
utilizar os repositories e manter a lógica de persistência centralizada.
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import SessionLocal


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Sessão async para ETL; faz commit em sucesso e rollback em erro."""
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
