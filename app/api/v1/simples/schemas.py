from datetime import date

from pydantic import BaseModel, ConfigDict


class SimplesRead(BaseModel):
    """Schema de leitura de Simples Nacional."""

    model_config = ConfigDict(from_attributes=True)

    cnpj_basico: str
    opcao_simples: str
    data_opcao_simples: date | None
    data_exclusao_simples: date | None
    opcao_mei: str
    data_opcao_mei: date | None
    data_exclusao_mei: date | None
