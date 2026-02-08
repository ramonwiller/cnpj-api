from pydantic import BaseModel, ConfigDict


class NaturezaRead(BaseModel):
    """Schema de leitura de natureza. Criação, atualização e exclusão via ETL."""

    model_config = ConfigDict(from_attributes=True)

    codigo: str
    descricao: str
