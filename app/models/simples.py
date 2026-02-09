from enum import Enum as PyEnum

from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Date
)

from app.core.database import Base


class OpcaoSimples(str, PyEnum):
    """Opção Simples Nacional conforme código da Receita Federal."""

    SIM = "S"
    NAO = "N"
    OUTROS = ""


class OpcaoMei(str, PyEnum):
    """Opção MEI conforme código da Receita Federal."""

    SIM = "S"
    NAO = "N"
    OUTROS = ""

class Simples(Base):
    """
    Simples Nacional da empresa.
    cnpj_basico pode repetir (uma empresa tem um Simples Nacional).
    """
    __tablename__ = 'simples'

    # Chave primária composta: o cnpj_basico é único;
    cnpj_basico = Column(String(10), ForeignKey('empresas.cnpj_basico'), nullable=False, primary_key=True)
    opcao_simples = Column(String(1), nullable=False, default=OpcaoSimples.OUTROS)
    data_opcao_simples = Column(Date, nullable=True)
    data_exclusao_simples = Column(Date, nullable=True)
    opcao_mei = Column(String(1), nullable=False, default=OpcaoMei.OUTROS)
    data_opcao_mei = Column(Date, nullable=True)
    data_exclusao_mei = Column(Date, nullable=True)

