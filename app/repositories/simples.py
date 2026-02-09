from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.pagination import paginate
from app.models.simples import Simples


class SimplesRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_cnpj_basico(self, cnpj_basico: str) -> Simples | None:
        result = await self.session.execute(
            select(Simples).where(Simples.cnpj_basico == cnpj_basico)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        page: int = 1,
        limit: int = 25,
    ) -> tuple[list[Simples], int, int]:
        stmt = select(Simples).order_by(Simples.cnpj_basico)
        return await paginate(self.session, stmt, page, limit)

    async def create(self, simples: Simples) -> Simples:
        self.session.add(simples)
        await self.session.flush()
        await self.session.refresh(simples)
        return simples

    async def update(self, simples: Simples) -> Simples:
        await self.session.flush()
        await self.session.refresh(simples)
        return simples

    async def delete(self, simples: Simples) -> None:
        await self.session.delete(simples)
        await self.session.flush()
