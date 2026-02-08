from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class EmpresaRead(BaseModel):
    """Schema de leitura de empresa."""

    model_config = ConfigDict(from_attributes=True)

    cnpj_basico: str
    razao_social: str
    natureza_juridica: str
    qualificacao_responsavel: str
    capital_social: Decimal
    porte_empresa: str
    ente_federativo: str | None
