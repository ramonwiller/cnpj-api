from pydantic import BaseModel, ConfigDict


class MunicipioRead(BaseModel):
    """Schema de leitura de municipio. Criação, atualização e exclusão via ETL."""

    model_config = ConfigDict(from_attributes=True)

    codigo: str
    descricao: str
