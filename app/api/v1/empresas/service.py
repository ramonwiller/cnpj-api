from sqlalchemy.ext.asyncio import AsyncSession

from app.models.empresa import Empresa
from app.repositories.empresa import EmpresaRepository


class EmpresaService:
    """Serviço de leitura de empresas."""

    def __init__(self, session: AsyncSession):
        self._repo = EmpresaRepository(session)

    async def get_by_cnpj_basico(self, cnpj_basico: str) -> Empresa | None:
        return await self._repo.get_by_cnpj_basico(cnpj_basico)

    async def get_all(self, page: int = 1, limit: int = 25):
        return await self._repo.get_all(page=page, limit=limit)
