from enum import Enum as PyEnum

from sqlalchemy import (
    Column,
    ForeignKey,
    Numeric,
    String,
)

from app.core.database import Base


class PorteEmpresa(str, PyEnum):
    """Porte da empresa conforme código da Receita Federal."""

    NAO_INFORMADO = "00"
    MICRO_EMPRESA = "01"
    EMPRESA_DE_PEQUENO_PORTE = "03"
    DEMAIS = "05"


class Empresa(Base):
    __tablename__ = 'empresas'

    cnpj_basico = Column(String(10), primary_key=True, nullable=False)
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
    

