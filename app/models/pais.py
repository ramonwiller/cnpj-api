from sqlalchemy import (
    Column,
    String,
)

from app.core.database import Base


class Pais(Base):
    __tablename__ = 'paises'

    codigo = Column(String(3), primary_key=True, nullable=False)
    descricao = Column(String, nullable=False)
