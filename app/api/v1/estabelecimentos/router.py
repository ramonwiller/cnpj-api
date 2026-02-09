from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.pagination import PaginatedResponse, get_pagination_params, PaginationParams
from app.api.v1.estabelecimentos.schemas import EstabelecimentoRead
from app.api.v1.estabelecimentos.service import EstabelecimentoService

router = APIRouter(prefix="/empresas/{cnpj_basico}/estabelecimentos", tags=["Estabelecimentos"])


def get_estabelecimento_service(
    session: AsyncSession = Depends(get_db),
) -> EstabelecimentoService:
    return EstabelecimentoService(session)


@router.get("", response_model=PaginatedResponse[EstabelecimentoRead])
async def listar_estabelecimentos(
    cnpj_basico: str,
    pagination: PaginationParams = Depends(get_pagination_params),
    service: EstabelecimentoService = Depends(get_estabelecimento_service),
):
    """Lista estabelecimentos (matriz e filiais) de uma empresa pelo CNPJ básico."""
    estabelecimentos, total_items, total_pages = await service.get_by_cnpj_basico(
        cnpj_basico=cnpj_basico,
        page=pagination.page,
        limit=pagination.limit,
    )
    return PaginatedResponse.from_page(
        data=estabelecimentos,
        total_items=total_items,
        current_page=pagination.page,
        items_per_page=pagination.limit,
    )

@router.get("/{cnpj_ordem}", response_model=PaginatedResponse[EstabelecimentoRead])
async def listar_estabelecimentos(
    cnpj_basico: str,
    cnpj_ordem: str,
    pagination: PaginationParams = Depends(get_pagination_params),
    service: EstabelecimentoService = Depends(get_estabelecimento_service),
):
    """Lista estabelecimentos (matriz e filiais) de uma empresa pelo CNPJ ordem."""
    estabelecimentos, total_items, total_pages = await service.get_by_cnpj_ordem(
        cnpj_basico=cnpj_basico,
        cnpj_ordem=cnpj_ordem,
        page=pagination.page,
        limit=pagination.limit,
    )
    return PaginatedResponse.from_page(
        data=estabelecimentos,
        total_items=total_items,
        current_page=pagination.page,
        items_per_page=pagination.limit,
    )