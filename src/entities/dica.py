from sqlalchemy import Column, Integer, Enum, Text
from src.entities.base import Base

class Dica(Base):
    __tablename__ = "dica"

    id = Column(Integer, primary_key=True, autoincrement=True)
    objetivo = Column(Enum('perder peso', 'ganhar massa muscular', 'manter peso'), nullable=False)
    texto = Column(Text, nullable=False)

    def __init__(self, objetivo, texto):
        self.objetivo = objetivo
        self.texto = texto
