from sqlalchemy import Column, Integer, String, Float, Enum, Text
from sqlalchemy.orm import relationship
from src.entities.base import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    idade = Column(Integer, nullable=False)
    peso = Column(Float, nullable=False)
    altura = Column(Float, nullable=False)
    objetivo = Column(Enum('perder peso', 'ganhar massa muscular', 'manter peso'), nullable=False)
    restricoes = Column(Text)

    progressos = relationship("Progresso", back_populates="usuario", cascade="all, delete")

    def __init__(self, nome, idade, peso, altura, objetivo, restricoes=None):
        self.nome = nome
        self.idade = idade
        self.peso = peso
        self.altura = altura
        self.objetivo = objetivo
        self.restricoes = restricoes
