from sqlalchemy.ext.asyncio import AsyncSession

from app.models.natureza import Natureza
from app.repositories.natureza import NaturezaRepository


class NaturezaService:
    """Serviço apenas de leitura. Criação, atualização e exclusão via ETL."""

    def __init__(self, session: AsyncSession):
        self._repo = NaturezaRepository(session)

    async def get_by_codigo(self, codigo: str) -> Natureza | None:
        return await self._repo.get_by_codigo(codigo)

    async def get_all(self, page: int = 1, limit: int = 25):
        return await self._repo.get_all(page=page, limit=limit)
