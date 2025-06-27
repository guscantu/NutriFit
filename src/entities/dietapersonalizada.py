from sqlalchemy import Column, Integer, Enum, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.entities.base import Base

class DietaPersonalizada(Base):
    __tablename__ = "dietapersonalizada"

    id = Column(Integer, primary_key=True, autoincrement=True)
    faixa_peso_id = Column(Integer, ForeignKey("faixapeso.id", ondelete="CASCADE"))
    faixa_altura_id = Column(Integer, ForeignKey("faixaaltura.id", ondelete="CASCADE"))
    faixa_idade_id = Column(Integer, ForeignKey("faixaidade.id", ondelete="CASCADE"))
    objetivo = Column(Enum('perder peso', 'ganhar massa muscular', 'manter peso'), nullable=False)
    restricao = Column(Text)
    descricao = Column(Text, nullable=False)

    refeicoes = relationship("RefeicaoPersonalizada", back_populates="dieta_personalizada", cascade="all, delete")

    def __init__(self, faixa_peso_id, faixa_altura_id, faixa_idade_id, objetivo, descricao, restricao=None):
        self.faixa_peso_id = faixa_peso_id
        self.faixa_altura_id = faixa_altura_id
        self.faixa_idade_id = faixa_idade_id
        self.objetivo = objetivo
        self.descricao = descricao
        self.restricao = restricao
