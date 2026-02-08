from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.pagination import PaginatedResponse, get_pagination_params, PaginationParams
from app.api.v1.empresas.schemas import EmpresaRead
from app.api.v1.empresas.service import EmpresaService

router = APIRouter(prefix="/empresas", tags=["Empresas"])


def get_empresa_service(session: AsyncSession = Depends(get_db)) -> EmpresaService:
    return EmpresaService(session)


@router.get("", response_model=PaginatedResponse[EmpresaRead])
async def listar_empresas(
    pagination: PaginationParams = Depends(get_pagination_params),
    service: EmpresaService = Depends(get_empresa_service),
):
    """Lista todas as empresas com paginação."""
    empresas, total_items, total_pages = await service.get_all(
        page=pagination.page, limit=pagination.limit
    )
    return PaginatedResponse.from_page(
        data=empresas,
        total_items=total_items,
        current_page=pagination.page,
        items_per_page=pagination.limit,
    )


@router.get("/{cnpj_basico}", response_model=EmpresaRead)
async def obter_empresa(
    cnpj_basico: str,
    service: EmpresaService = Depends(get_empresa_service),
):
    """Retorna uma empresa pelo CNPJ básico (8 primeiros dígitos do CNPJ)."""
    empresa = await service.get_by_cnpj_basico(cnpj_basico)
    if empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return empresa
