from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.naturezas.schemas import NaturezaRead
from app.api.v1.naturezas.service import NaturezaService
from app.core.database import get_db
from app.core.pagination import PaginatedResponse, PaginationParams, get_pagination_params

router = APIRouter(prefix="/naturezas_juridicas", tags=["Tabelas de Domínios"])


def get_natureza_service(session: AsyncSession = Depends(get_db)) -> NaturezaService:
    return NaturezaService(session)


@router.get("", response_model=PaginatedResponse[NaturezaRead])
async def listar_naturezas(
    pagination: PaginationParams = Depends(get_pagination_params),
    service: NaturezaService = Depends(get_natureza_service),
):
    """Lista todos as naturezas. Dados mantidos via ETL."""
    naturezas, total_items, total_pages = await service.get_all(
        page=pagination.page, limit=pagination.limit
    )
    return PaginatedResponse.from_page(
        data=naturezas,
        total_items=total_items,
        current_page=pagination.page,
        items_per_page=pagination.limit,
    )


@router.get("/{codigo}", response_model=NaturezaRead)
async def obter_natureza(codigo: str, service: NaturezaService = Depends(get_natureza_service)):
    """Retorna uma natureza pelo código (ex: 1234567). Dados mantidos via ETL."""
    natureza = await service.get_by_codigo(codigo)
    if natureza is None:
        raise HTTPException(status_code=404, detail="Natureza não encontrado")
    return natureza
