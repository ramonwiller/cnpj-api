from pydantic import BaseModel, ConfigDict


class PaisRead(BaseModel):
    """Schema de leitura de país. Criação, atualização e exclusão via ETL."""

    model_config = ConfigDict(from_attributes=True)

    codigo: str
    descricao: str
