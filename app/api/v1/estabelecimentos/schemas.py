from datetime import date

from pydantic import BaseModel, ConfigDict


class EstabelecimentoRead(BaseModel):
    """Schema de leitura de estabelecimento."""

    model_config = ConfigDict(from_attributes=True)

    cnpj_basico: str
    cnpj_ordem: str
    cnpj_dv: str
    identificador_matriz_filial: str
    nome_fantasia: str
    situacao_cadastral: str
    data_situacao_cadastral: date
    motivo_situacao_cadastral: str
    nome_cidade_exterior: str | None
    pais: str | None
    data_inicio_atividade: date | None
    cnae_fiscal_principal: str
    cnae_fiscal_secundaria: str | None
    tipo_logradouro: str
    logradouro: str
    numero: str
    complemento: str | None
    bairro: str
    cep: str
    uf: str
    municipio: str
    ddd1: str | None
    telefone1: str | None
    ddd2: str | None
    telefone2: str | None
    ddd_fax: str | None
    fax: str | None
    correio_eletronico: str | None
    situacao_especial: str | None
    data_situacao_especial: date | None
