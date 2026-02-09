from pydantic import BaseModel, ConfigDict


class MotivoRead(BaseModel):
    """Schema de leitura de motivo. Criação, atualização e exclusão via ETL."""

    model_config = ConfigDict(from_attributes=True)

    codigo: str
    descricao: str
