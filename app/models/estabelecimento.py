from enum import Enum as PyEnum

from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Date
)

from app.core.database import Base


class IdentificadorMatrizFilial(str, PyEnum):
    """Identificador da matriz ou filial conforme código da Receita Federal."""

    MATRIZ = "1"
    FILIAL = "2"


class SituacaoCadastral(str, PyEnum):
    """Situação cadastral conforme código da Receita Federal."""

    NULA = "01"
    ATIVA = "02"
    SUSPENSA = "03"
    INAPTA = "04"
    BAIXADA = "08"

class Estabelecimento(Base):
    """
    Estabelecimento (matriz/filial) da empresa.
    cnpj_basico pode repetir (uma empresa tem vários estabelecimentos).
    A combinação (cnpj_basico, cnpj_ordem, cnpj_dv) é única.
    """
    __tablename__ = 'estabelecimentos'

    # Chave primária composta: os 3 juntos são únicos;
    cnpj_basico = Column(String(10), ForeignKey('empresas.cnpj_basico'), nullable=False, primary_key=True)
    cnpj_ordem = Column(String(4), primary_key=True, nullable=False)
    cnpj_dv = Column(String(2), primary_key=True, nullable=False)
    identificador_matriz_filial = Column(String(1), nullable=False, default=IdentificadorMatrizFilial.MATRIZ)
    nome_fantasia = Column(String, nullable=False)
    situacao_cadastral = Column(String(2), nullable=False, default=SituacaoCadastral.NULA)
    data_situacao_cadastral = Column(Date, nullable=False)
    motivo_situacao_cadastral = Column(
        String(7),
        ForeignKey('motivos.codigo'),
        nullable=False,
    )
    nome_cidade_exterior = Column(String, nullable=True)
    pais = Column(
        String(7),
        ForeignKey('paises.codigo'),
        nullable=True,
    )
    data_inicio_atividade = Column(Date, nullable=True)
    cnae_fiscal_principal = Column(
        String(7),
        ForeignKey('cnaes.codigo'),
        nullable=False,
    )
    cnae_fiscal_secundaria = Column(String, nullable=True)
    tipo_logradouro = Column(String, nullable=False)
    logradouro = Column(String, nullable=False)
    numero = Column(String, nullable=False)
    complemento = Column(String, nullable=True)
    bairro = Column(String, nullable=False)
    cep = Column(String(8), nullable=False)
    uf = Column(String(2), nullable=False)
    municipio = Column(
        String(7),
        ForeignKey('municipios.codigo'),
        nullable=False,
    )
    ddd1 = Column(String(2), nullable=True)
    telefone1 = Column(String, nullable=True)
    ddd2 = Column(String(2), nullable=True)
    telefone2 = Column(String, nullable=True)
    ddd_fax = Column(String(2), nullable=True)
    fax = Column(String, nullable=True)
    correio_eletronico = Column(String, nullable=True)
    situacao_especial = Column(String, nullable=True)
    data_situacao_especial = Column(Date, nullable=True)