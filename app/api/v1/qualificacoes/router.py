from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.qualificacoes.schemas import QualificacaoRead
from app.api.v1.qualificacoes.service import QualificacaoService
from app.core.database import get_db
from app.core.pagination import PaginatedResponse, PaginationParams, get_pagination_params

router = APIRouter(prefix="/qualificacoes_socios", tags=["Tabelas de Domínios"])


def get_qualificacao_service(session: AsyncSession = Depends(get_db)) -> QualificacaoService:
    return QualificacaoService(session)


@router.get("", response_model=PaginatedResponse[QualificacaoRead])
async def listar_qualificacoes(
    pagination: PaginationParams = Depends(get_pagination_params),
    service: QualificacaoService = Depends(get_qualificacao_service),
):
    """Lista todos as qualificacoes. Dados mantidos via ETL."""
    qualificacoes, total_items, total_pages = await service.get_all(
        page=pagination.page, limit=pagination.limit
    )
    return PaginatedResponse.from_page(
        data=qualificacoes,
        total_items=total_items,
        current_page=pagination.page,
        items_per_page=pagination.limit,
    )


@router.get("/{codigo}", response_model=QualificacaoRead)
async def obter_qualificacao(codigo: str, service: QualificacaoService = Depends(get_qualificacao_service)):
    """Retorna uma qualificacao pelo código (ex: 1234567). Dados mantidos via ETL."""
    qualificacao = await service.get_by_codigo(codigo)
    if qualificacao is None:
        raise HTTPException(status_code=404, detail="Qualificacao não encontrado")
    return qualificacao
