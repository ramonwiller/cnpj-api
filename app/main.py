from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1 import router as v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


API_DESCRIPTION = """
Este projeto open source disponibiliza uma API REST para consulta programática aos dados do Cadastro Nacional da Pessoa Jurídica (CNPJ), com base nas informações públicas fornecidas pela Secretaria Especial da Receita Federal do Brasil (RFB).

A API permite acessar, de forma simples e padronizada, informações cadastrais de pessoas jurídicas e outras entidades registradas no CNPJ, utilizando endpoints REST que consultam diretamente um banco de dados estruturado a partir da base oficial.

O objetivo do projeto é facilitar o consumo dessas informações por sistemas, aplicações e integrações, promovendo transparência, reutilização de dados públicos e desenvolvimento de soluções abertas para consulta de dados cadastrais empresariais no Brasil.
"""


def create_app() -> FastAPI:
    app = FastAPI(
        title="CNPJ API",
        description=API_DESCRIPTION,
        version=settings.api_version,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    @app.get("/health", include_in_schema=False)
    async def health():
        return {"status": "ok"}

    app.include_router(v1_router, prefix="/api")

    return app


app = create_app()