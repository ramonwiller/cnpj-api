from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.municipios.schemas import MunicipioRead
from app.api.v1.municipios.service import MunicipioService
from app.core.database import get_db
from app.core.pagination import PaginatedResponse, PaginationParams, get_pagination_params

router = APIRouter(prefix="/municipios", tags=["Tabelas de Domínios"])


def get_municipio_service(session: AsyncSession = Depends(get_db)) -> MunicipioService:
    return MunicipioService(session)


@router.get("", response_model=PaginatedResponse[MunicipioRead])
async def listar_municipios(
    pagination: PaginationParams = Depends(get_pagination_params),
    service: MunicipioService = Depends(get_municipio_service),
):
    """Lista todos os municipios. Dados mantidos via ETL."""
    municipios, total_items, total_pages = await service.get_all(
        page=pagination.page, limit=pagination.limit
    )
    return PaginatedResponse.from_page(
        data=municipios,
        total_items=total_items,
        current_page=pagination.page,
        items_per_page=pagination.limit,
    )


@router.get("/{codigo}", response_model=MunicipioRead)
async def obter_municipio(codigo: str, service: MunicipioService = Depends(get_municipio_service)):
    """Retorna um municipio pelo código (ex: 1234567). Dados mantidos via ETL."""
    municipio = await service.get_by_codigo(codigo)
    if municipio is None:
        raise HTTPException(status_code=404, detail="Municipio não encontrado")
    return municipio
