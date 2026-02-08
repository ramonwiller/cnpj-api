from sqlalchemy.ext.asyncio import AsyncSession

from app.models.municipio import Municipio
from app.repositories.municipio import MunicipioRepository


class MunicipioService:
    """Serviço apenas de leitura. Criação, atualização e exclusão via ETL."""

    def __init__(self, session: AsyncSession):
        self._repo = MunicipioRepository(session)

    async def get_by_codigo(self, codigo: str) -> Municipio | None:
        return await self._repo.get_by_codigo(codigo)

    async def get_all(self, page: int = 1, limit: int = 25):
        return await self._repo.get_all(page=page, limit=limit)
