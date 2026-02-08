from fastapi import APIRouter

from app.api.v1.paises import router as paises_router
from app.api.v1.municipios import router as municipios_router
from app.api.v1.qualificacoes import router as qualificacoes_router
from app.api.v1.naturezas import router as naturezas_router
from app.api.v1.cnaes import router as cnaes_router

router = APIRouter(prefix="/v1")
router.include_router(paises_router)
router.include_router(municipios_router)
router.include_router(qualificacoes_router)
router.include_router(naturezas_router)
router.include_router(cnaes_router)