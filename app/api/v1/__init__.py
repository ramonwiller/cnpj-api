from fastapi import APIRouter

from app.api.v1.cnaes import router as cnaes_router
from app.api.v1.empresas import router as empresas_router
from app.api.v1.estabelecimentos import router as estabelecimentos_router
from app.api.v1.municipios import router as municipios_router
from app.api.v1.naturezas import router as naturezas_router
from app.api.v1.paises import router as paises_router
from app.api.v1.qualificacoes import router as qualificacoes_router

router = APIRouter(prefix="/v1")
router.include_router(paises_router)
router.include_router(municipios_router)
router.include_router(qualificacoes_router)
router.include_router(naturezas_router)
router.include_router(cnaes_router)
router.include_router(empresas_router)
router.include_router(estabelecimentos_router)