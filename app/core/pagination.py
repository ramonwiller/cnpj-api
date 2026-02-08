"""Helpers e schemas de paginação reutilizáveis."""

from typing import Any, Generic, Optional, TypeVar

from fastapi import Query
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from app.core.config import settings

T = TypeVar("T")


# ------ Schemas ------

class PaginationParams(BaseModel):
    """Parâmetros de paginação (query: page, limit)."""

    page: int = Field(default=1, ge=1, description="Página (1-based)")
    limit: int = Field(
        default=25,
        ge=1,
        le=100,
        description="Itens por página",
    )


def get_pagination_params(
    page: int = Query(1, ge=1, description="Página"),
    limit: int = Query(
        settings.page_limit,
        ge=1,
        le=100,
        description="Itens por página",
    ),
) -> PaginationParams:
    """Dependency para FastAPI: use com Depends(get_pagination_params)."""
    return PaginationParams(page=page, limit=limit)


class PaginatedResponse(BaseModel, Generic[T]):
    """Resposta paginada padrão: data + metadados."""

    data: list[T] = Field(default_factory=list)
    total_items: int = Field(..., ge=0, description="Total de itens")
    items_per_page: int = Field(..., ge=1, description="Itens por página")
    total_pages: int = Field(..., ge=0, description="Total de páginas")
    current_page: int = Field(..., ge=1, description="Página atual")
    has_next_page: bool = Field(..., description="Existe página seguinte")
    has_previous_page: bool = Field(..., description="Existe página anterior")
    next_page: Optional[int] = Field(None, description="Número da próxima página")
    previous_page: Optional[int] = Field(None, description="Número da página anterior")

    @classmethod
    def from_page(
        cls,
        data: list[T],
        total_items: int,
        current_page: int,
        items_per_page: int,
    ) -> "PaginatedResponse[T]":
        """Constrói a resposta a partir de data e parâmetros da página."""
        total_pages = total_pages_from(total_items, items_per_page)
        has_next = current_page < total_pages
        has_prev = current_page > 1
        return cls(
            data=data,
            total_items=total_items,
            items_per_page=items_per_page,
            total_pages=total_pages,
            current_page=current_page,
            has_next_page=has_next,
            has_previous_page=has_prev,
            next_page=current_page + 1 if has_next else None,
            previous_page=current_page - 1 if has_prev else None,
        )


# ------ Funções puras ------

def get_offset(page: int, limit: int) -> int:
    """Calcula offset (0-based) a partir de page (1-based) e limit."""
    return (page - 1) * limit


def total_pages_from(total_items: int, limit: int) -> int:
    """Calcula total de páginas. Retorna 0 se total_items == 0."""
    if total_items <= 0:
        return 0
    return (total_items + limit - 1) // limit


# ------ Helper SQLAlchemy ------

async def paginate(
    session: AsyncSession,
    stmt: Select[Any],
    page: int,
    limit: int,
) -> tuple[list[Any], int, int]:
    """
    Executa um SELECT paginado e retorna (items, total_items, total_pages).

    O count é feito sobre o mesmo conjunto de linhas do select (subquery),
    então filtros e joins são respeitados. Ordenação não afeta o count.
    """
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total_items = (await session.scalar(count_stmt)) or 0
    offset = get_offset(page, limit)
    result = await session.execute(stmt.offset(offset).limit(limit))
    items = list(result.scalars().all())
    total_pages = total_pages_from(total_items, limit)
    return items, total_items, total_pages
