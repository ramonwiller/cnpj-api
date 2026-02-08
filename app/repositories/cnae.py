from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.pagination import paginate
from app.models.cnae import Cnae


class CnaeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_codigo(self, codigo: str) -> Cnae | None:
        result = await self.session.execute(
            select(Cnae).where(Cnae.codigo == codigo)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        page: int = 1,
        limit: int = 25,
    ) -> tuple[list[Cnae], int, int]:
        stmt = select(Cnae).order_by(Cnae.codigo)
        return await paginate(self.session, stmt, page, limit)


    async def create(self, cnae: Cnae) -> Cnae:
        self.session.add(cnae)
        await self.session.flush()
        await self.session.refresh(cnae)
        return cnae

    async def update(self, cnae: Cnae) -> Cnae:
        await self.session.flush()
        await self.session.refresh(cnae)
        return cnae

    async def delete(self, cnae: Cnae) -> None:
        await self.session.delete(cnae)
        await self.session.flush()
