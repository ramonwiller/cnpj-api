from sqlalchemy.ext.asyncio import AsyncSession

from app.models.motivo import Motivo
from app.repositories.motivo import MotivoRepository
class MotivoService:
    """Serviço apenas de leitura. Criação, atualização e exclusão via ETL."""

    def __init__(self, session: AsyncSession):
        self._repo = MotivoRepository(session)

    async def get_by_codigo(self, codigo: str) -> Motivo | None:
        return await self._repo.get_by_codigo(codigo)

    async def get_all(self, page: int = 1, limit: int = 25):
        return await self._repo.get_all(page=page, limit=limit)
