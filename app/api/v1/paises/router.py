from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.paises.schemas import PaisRead
from app.api.v1.paises.service import PaisService
from app.core.database import get_db
from app.core.pagination import PaginatedResponse, PaginationParams, get_pagination_params

router = APIRouter(prefix="/paises", tags=["Tabelas de Domínios"])


def get_pais_service(session: AsyncSession = Depends(get_db)) -> PaisService:
    return PaisService(session)


@router.get("", response_model=PaginatedResponse[PaisRead])
async def listar_paises(
    pagination: PaginationParams = Depends(get_pagination_params),
    service: PaisService = Depends(get_pais_service),
):
    """Lista todos os países. Dados mantidos via ETL."""
    paises, total_items, total_pages = await service.get_all(
        page=pagination.page, limit=pagination.limit
    )
    return PaginatedResponse.from_page(
        data=paises,
        total_items=total_items,
        current_page=pagination.page,
        items_per_page=pagination.limit,
    )


@router.get("/{codigo}", response_model=PaisRead)
async def obter_pais(codigo: str, service: PaisService = Depends(get_pais_service)):
    """Retorna um país pelo código (ex: BRA). Dados mantidos via ETL."""
    pais = await service.get_by_codigo(codigo)
    if pais is None:
        raise HTTPException(status_code=404, detail="País não encontrado")
    return pais
