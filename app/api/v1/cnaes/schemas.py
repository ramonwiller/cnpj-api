from pydantic import BaseModel, ConfigDict


class CnaeRead(BaseModel):
    """Schema de leitura de cnae. Criação, atualização e exclusão via ETL."""

    model_config = ConfigDict(from_attributes=True)

    codigo: str
    descricao: str
