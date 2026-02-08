from sqlalchemy import (
    Column,
    String,
)

from app.core.database import Base


class Natureza(Base):
    __tablename__ = 'naturezas'

    codigo = Column(String(7), primary_key=True, nullable=False)
    descricao = Column(String, nullable=False)

