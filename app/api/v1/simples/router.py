from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.pagination import PaginatedResponse, get_pagination_params, PaginationParams
from app.api.v1.simples.schemas import SimplesRead
from app.api.v1.simples.service import SimplesService

router = APIRouter(prefix="/simples", tags=["Simples Nacional"])


def get_simples_service(session: AsyncSession = Depends(get_db)) -> SimplesService:
    return SimplesService(session)


@router.get("", response_model=PaginatedResponse[SimplesRead])
async def listar_simples(
    pagination: PaginationParams = Depends(get_pagination_params),
    service: SimplesService = Depends(get_simples_service),
):
    """Lista todos os registros de Simples Nacional com paginação."""
    itens, total_items, total_pages = await service.get_all(
        page=pagination.page, limit=pagination.limit
    )
    return PaginatedResponse.from_page(
        data=itens,
        total_items=total_items,
        current_page=pagination.page,
        items_per_page=pagination.limit,
    )


@router.get("/{cnpj_basico}", response_model=SimplesRead)
async def obter_simples(
    cnpj_basico: str,
    service: SimplesService = Depends(get_simples_service),
):
    """Retorna o Simples Nacional de uma empresa pelo CNPJ básico (8 primeiros dígitos do CNPJ)."""
    simples = await service.get_by_cnpj_basico(cnpj_basico)
    if simples is None:
        raise HTTPException(status_code=404, detail="Simples Nacional não encontrado")
    return simples
