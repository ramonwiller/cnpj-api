from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.pagination import paginate
from app.models.pais import Pais


class PaisRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_codigo(self, codigo: str) -> Pais | None:
        result = await self.session.execute(
            select(Pais).where(Pais.codigo == codigo)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        page: int = 1,
        limit: int = 25,
    ) -> tuple[list[Pais], int, int]:
        stmt = select(Pais).order_by(Pais.codigo)
        return await paginate(self.session, stmt, page, limit)

    async def create(self, pais: Pais) -> Pais:
        self.session.add(pais)
        await self.session.flush()
        await self.session.refresh(pais)
        return pais

    async def update(self, pais: Pais) -> Pais:
        await self.session.flush()
        await self.session.refresh(pais)
        return pais

    async def delete(self, pais: Pais) -> None:
        await self.session.delete(pais)
        await self.session.flush()
