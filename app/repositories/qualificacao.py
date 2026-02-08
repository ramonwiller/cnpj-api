from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.pagination import paginate
from app.models.qualificacao import Qualificacao


class QualificacaoRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_codigo(self, codigo: str) -> Qualificacao | None:
        result = await self.session.execute(
            select(Qualificacao).where(Qualificacao.codigo == codigo)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        page: int = 1,
        limit: int = 25,
    ) -> tuple[list[Qualificacao], int, int]:
        stmt = select(Qualificacao).order_by(Qualificacao.codigo)
        return await paginate(self.session, stmt, page, limit)

    async def create(self, qualificacao: Qualificacao) -> Qualificacao:
        self.session.add(qualificacao)
        await self.session.flush()
        await self.session.refresh(qualificacao)
        return qualificacao

    async def update(self, qualificacao: Qualificacao) -> Qualificacao:
        await self.session.flush()
        await self.session.refresh(qualificacao)
        return qualificacao

    async def delete(self, qualificacao: Qualificacao) -> None:
        await self.session.delete(qualificacao)
        await self.session.flush()
