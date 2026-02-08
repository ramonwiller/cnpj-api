from sqlalchemy import (
    Column,
    String,
)

from app.core.database import Base


class Municipio(Base):
    __tablename__ = 'municipios'

    codigo = Column(String(7), primary_key=True, nullable=False)
    descricao = Column(String, nullable=False)

