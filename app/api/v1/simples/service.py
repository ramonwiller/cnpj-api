from sqlalchemy.ext.asyncio import AsyncSession

from app.models.simples import Simples
from app.repositories.simples import SimplesRepository


class SimplesService:
    """Serviço de leitura de Simples Nacional."""

    def __init__(self, session: AsyncSession):
        self._repo = SimplesRepository(session)

    async def get_by_cnpj_basico(self, cnpj_basico: str) -> Simples | None:
        return await self._repo.get_by_cnpj_basico(cnpj_basico)

    async def get_all(self, page: int = 1, limit: int = 25):
        return await self._repo.get_all(page=page, limit=limit)
