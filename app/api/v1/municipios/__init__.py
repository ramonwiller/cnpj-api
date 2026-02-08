from app.api.v1.municipios.router import router
from app.api.v1.municipios.schemas import MunicipioRead
from app.api.v1.municipios.service import MunicipioService

__all__ = ["router", "MunicipioRead", "MunicipioService"]
