from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.pagination import paginate
from app.models.natureza import Natureza


class NaturezaRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_codigo(self, codigo: str) -> Natureza | None:
        result = await self.session.execute(
            select(Natureza).where(Natureza.codigo == codigo)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        page: int = 1,
        limit: int = 25,
    ) -> tuple[list[Natureza], int, int]:
        stmt = select(Natureza).order_by(Natureza.codigo)
        return await paginate(self.session, stmt, page, limit)

    async def create(self, natureza: Natureza) -> Natureza:
        self.session.add(natureza)
        await self.session.flush()
        await self.session.refresh(natureza)
        return natureza

    async def update(self, natureza: Natureza) -> Natureza:
        await self.session.flush()
        await self.session.refresh(natureza)
        return natureza

    async def delete(self, natureza: Natureza) -> None:
        await self.session.delete(natureza)
        await self.session.flush()
