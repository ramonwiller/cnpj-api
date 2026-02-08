from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.pagination import PaginatedResponse, get_pagination_params, PaginationParams
from app.api.v1.cnaes.schemas import CnaeRead
from app.api.v1.cnaes.service import CnaeService

router = APIRouter(prefix="/cnaes", tags=["Tabelas de Domínios"])


def get_cnae_service(session: AsyncSession = Depends(get_db)) -> CnaeService:
    return CnaeService(session)


@router.get("", response_model=PaginatedResponse[CnaeRead])
async def listar_cnaes(
    pagination: PaginationParams = Depends(get_pagination_params),
    service: CnaeService = Depends(get_cnae_service),
):
    """Lista todos os cnaes. Dados mantidos via ETL."""
    cnaes, total_items, total_pages = await service.get_all(
        page=pagination.page, limit=pagination.limit
    )
    return PaginatedResponse.from_page(
        data=cnaes,
        total_items=total_items,
        current_page=pagination.page,
        items_per_page=pagination.limit,
    )


@router.get("/{codigo}", response_model=CnaeRead)
async def obter_cnae(
    codigo: str, 
    service: CnaeService = Depends(get_cnae_service)
):
    """Retorna um cnae pelo código (ex: 1234567). Dados mantidos via ETL."""
    cnae = await service.get_by_codigo(codigo)
    if cnae is None:
        raise HTTPException(status_code=404, detail="Cnae não encontrado")
    return cnae


