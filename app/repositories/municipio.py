from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.pagination import paginate
from app.models.municipio import Municipio


class MunicipioRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_codigo(self, codigo: str) -> Municipio | None:
        result = await self.session.execute(
            select(Municipio).where(Municipio.codigo == codigo)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        page: int = 1,
        limit: int = 25,
    ) -> tuple[list[Municipio], int, int]:
        stmt = select(Municipio).order_by(Municipio.codigo)
        return await paginate(self.session, stmt, page, limit)

    async def create(self, municipio: Municipio) -> Municipio:
        self.session.add(municipio)
        await self.session.flush()
        await self.session.refresh(municipio)
        return municipio

    async def update(self, municipio: Municipio) -> Municipio:
        await self.session.flush()
        await self.session.refresh(municipio)
        return municipio

    async def delete(self, municipio: Municipio) -> None:
        await self.session.delete(municipio)
        await self.session.flush()
