from sqlalchemy.ext.asyncio import AsyncSession

from app.models.estabelecimento import Estabelecimento
from app.repositories.estabelecimento import EstabelecimentoRepository


class EstabelecimentoService:
    """Serviço de leitura de estabelecimentos."""

    def __init__(self, session: AsyncSession):
        self._repo = EstabelecimentoRepository(session)

    async def get_by_cnpj(
        self,
        cnpj_basico: str,
        cnpj_ordem: str,
        cnpj_dv: str,
    ) -> Estabelecimento | None:
        return await self._repo.get_by_cnpj(
            cnpj_basico=cnpj_basico,
            cnpj_ordem=cnpj_ordem,
            cnpj_dv=cnpj_dv,
        )

    async def get_by_cnpj_basico(
        self,
        cnpj_basico: str,
        page: int = 1,
        limit: int = 25,
    ):
        return await self._repo.get_by_cnpj_basico(
            cnpj_basico=cnpj_basico,
            page=page,
            limit=limit,
        )

    async def get_all(self, page: int = 1, limit: int = 25):
        return await self._repo.get_all(page=page, limit=limit)
