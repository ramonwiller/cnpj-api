from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.pagination import PaginatedResponse, get_pagination_params, PaginationParams
from app.api.v1.motivos.schemas import MotivoRead
from app.api.v1.motivos.service import MotivoService

router = APIRouter(prefix="/motivos", tags=["Tabelas de Domínios"])


def get_motivo_service(session: AsyncSession = Depends(get_db)) -> MotivoService:
    return MotivoService(session)


@router.get("", response_model=PaginatedResponse[MotivoRead])
async def listar_motivos(
    pagination: PaginationParams = Depends(get_pagination_params),
    service: MotivoService = Depends(get_motivo_service),
):
    """Lista todos os motivos. Dados mantidos via ETL."""
    motivos, total_items, total_pages = await service.get_all(
        page=pagination.page, limit=pagination.limit
    )
    return PaginatedResponse.from_page(
        data=motivos,
        total_items=total_items,
        current_page=pagination.page,
        items_per_page=pagination.limit,
    )


@router.get("/{codigo}", response_model=MotivoRead)
async def obter_motivo(
    codigo: str, 
    service: MotivoService = Depends(get_motivo_service)
):
    """Retorna um motivo pelo código (ex: 1234567). Dados mantidos via ETL."""
    motivo = await service.get_by_codigo(codigo)
    if motivo is None:
        raise HTTPException(status_code=404, detail="Motivo não encontrado")
    return motivo


