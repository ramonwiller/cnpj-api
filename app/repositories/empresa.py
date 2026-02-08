from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.pagination import paginate
from app.models.empresa import Empresa


class EmpresaRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_cnpj_basico(self, cnpj_basico: str) -> Empresa | None:
        result = await self.session.execute(
            select(Empresa).where(Empresa.cnpj_basico == cnpj_basico)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        page: int = 1,
        limit: int = 25,
    ) -> tuple[list[Empresa], int, int]:
        stmt = select(Empresa).order_by(Empresa.cnpj_basico)
        return await paginate(self.session, stmt, page, limit)

    async def create(self, empresa: Empresa) -> Empresa:
        self.session.add(empresa)
        await self.session.flush()
        await self.session.refresh(empresa)
        return empresa

    async def update(self, empresa: Empresa) -> Empresa:
        await self.session.flush()
        await self.session.refresh(empresa)
        return empresa

    async def delete(self, empresa: Empresa) -> None:
        await self.session.delete(empresa)
        await self.session.flush()
