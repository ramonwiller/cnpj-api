from enum import Enum as PyEnum

from sqlalchemy import (
    Column,
    ForeignKey,
    Numeric,
    String,
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
    __tablename__ = 'estabelecimentos'

    cnpj_basico = Column(String(10), primary_key=True, nullable=False)
    cnpj_ordem = Column(String(4), nullable=False)
    cnpj_dv = Column(String(2), nullable=False)
    identificador_matriz_filial = Column(String(1), nullable=False, default=IdentificadorMatrizFilial.MATRIZ)
    nome_fantasia = Column(String, nullable=False)
    situacao_cadastral = Column(String(2), nullable=False, default=SituacaoCadastral.NULA)
    data_situacao_cadastral = Column(Date, nullable=False)
    motivo_situacao_cadastral = Column(String(2), nullable=False)
    nome_cidade_exterior = Column(String, nullable=True)
    pais = Column(String(3), nullable=True)
    data_inicio_atividade = Column(Date, nullable=True)
    cnae_fiscal = Column(String(7), nullable=True)
    cnae_fiscal_descricao = Column(String, nullable=True)
    cpf_representante_legal = Column(String(11), nullable=True)
    nome_representante_legal = Column(String, nullable=True)

    razao_social = Column(String, nullable=False)
    natureza_juridica = Column(
        String(7),
        ForeignKey('naturezas.codigo'),
        nullable=False,
    )
    qualificacao_responsavel = Column(
        String(7),
        ForeignKey('qualificacoes.codigo'),
        nullable=False,
    )
    capital_social = Column(Numeric(15, 2), nullable=False, default=0.00)
    porte_empresa = Column(String(2), nullable=False, default=PorteEmpresa.NAO_INFORMADO)
    ente_federativo = Column(String, nullable=True)
    

