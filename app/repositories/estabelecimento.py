from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.pagination import paginate
from app.models.estabelecimento import Estabelecimento


class EstabelecimentoRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_cnpj_ordem(
        self,
        cnpj_basico: str,
        cnpj_ordem: str,
    ) -> Estabelecimento | None:
        result = await self.session.execute(
            select(Estabelecimento).where(
                Estabelecimento.cnpj_basico == cnpj_basico,
                Estabelecimento.cnpj_ordem == cnpj_ordem,
            )
        )
        return result.scalar_one_or_none()

    async def get_by_cnpj_basico(
        self,
        cnpj_basico: str,
        page: int = 1,
        limit: int = 25,
    ) -> tuple[list[Estabelecimento], int, int]:
        stmt = (
            select(Estabelecimento)
            .where(Estabelecimento.cnpj_basico == cnpj_basico)
            .order_by(Estabelecimento.cnpj_ordem, Estabelecimento.cnpj_dv)
        )
        return await paginate(self.session, stmt, page, limit)

    async def get_all(
        self,
        page: int = 1,
        limit: int = 25,
    ) -> tuple[list[Estabelecimento], int, int]:
        stmt = select(Estabelecimento).order_by(
            Estabelecimento.cnpj_basico,
            Estabelecimento.cnpj_ordem,
            Estabelecimento.cnpj_dv,
        )
        return await paginate(self.session, stmt, page, limit)

    async def create(self, estabelecimento: Estabelecimento) -> Estabelecimento:
        self.session.add(estabelecimento)
        await self.session.flush()
        await self.session.refresh(estabelecimento)
        return estabelecimento

    async def update(self, estabelecimento: Estabelecimento) -> Estabelecimento:
        await self.session.flush()
        await self.session.refresh(estabelecimento)
        return estabelecimento

    async def delete(self, estabelecimento: Estabelecimento) -> None:
        await self.session.delete(estabelecimento)
        await self.session.flush()
