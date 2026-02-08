from app.api.v1.naturezas.router import router
from app.api.v1.naturezas.schemas import NaturezaRead
from app.api.v1.naturezas.service import NaturezaService

__all__ = ["router", "NaturezaRead", "NaturezaService"]
