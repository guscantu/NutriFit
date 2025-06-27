from sqlalchemy import Column, Integer, Float
from src.entities.base import Base

class FaixaPeso(Base):
    __tablename__ = "faixapeso"

    id = Column(Integer, primary_key=True, autoincrement=True)
    faixa_min = Column(Float, nullable=False)
    faixa_max = Column(Float, nullable=False)

    def __init__(self, faixa_min, faixa_max):
        self.faixa_min = faixa_min
        self.faixa_max = faixa_max
