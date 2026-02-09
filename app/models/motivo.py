from sqlalchemy import (
    Column,
    String,
)

from app.core.database import Base


class Motivo(Base):
    __tablename__ = 'motivos'

    codigo = Column(String(7), primary_key=True, nullable=False)
    descricao = Column(String, nullable=False)

