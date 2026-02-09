from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.pagination import paginate
from app.models.motivo import Motivo


class MotivoRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_codigo(self, codigo: str) -> Motivo | None:
        result = await self.session.execute(
            select(Motivo).where(Motivo.codigo == codigo)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        page: int = 1,
        limit: int = 25,
    ) -> tuple[list[Motivo], int, int]:
        stmt = select(Motivo).order_by(Motivo.codigo)
        return await paginate(self.session, stmt, page, limit)


    async def create(self, motivo: Motivo) -> Motivo:
        self.session.add(motivo)
        await self.session.flush()
        await self.session.refresh(motivo)
        return motivo

    async def update(self, motivo: Motivo) -> Motivo:
        await self.session.flush()
        await self.session.refresh(motivo)
        return motivo

    async def delete(self, motivo: Motivo) -> None:
        await self.session.delete(motivo)
        await self.session.flush()
