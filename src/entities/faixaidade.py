from sqlalchemy import Column, Integer
from src.entities.base import Base

class FaixaIdade(Base):
    __tablename__ = "faixaidade"

    id = Column(Integer, primary_key=True, autoincrement=True)
    faixa_min = Column(Integer, nullable=False)
    faixa_max = Column(Integer, nullable=False)

    def __init__(self, faixa_min, faixa_max):
        self.faixa_min = faixa_min
        self.faixa_max = faixa_max
