from sqlalchemy import Column, Integer, String
from src.entities.base import Base

class RestricaoAlimentar(Base):
    __tablename__ = "restricaoalimentar"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)

    def __init__(self, nome):
        self.nome = nome
