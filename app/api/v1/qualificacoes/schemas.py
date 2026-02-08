from pydantic import BaseModel, ConfigDict


class QualificacaoRead(BaseModel):
    """Schema de leitura de qualificacao. Criação, atualização e exclusão via ETL."""

    model_config = ConfigDict(from_attributes=True)

    codigo: str
    descricao: str
