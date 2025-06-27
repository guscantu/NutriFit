from sqlalchemy import Column, Integer, Enum, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.entities.base import Base

class RefeicaoPersonalizada(Base):
    __tablename__ = "refeicaopersonalizada"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dieta_personalizada_id = Column(Integer, ForeignKey("dietapersonalizada.id", ondelete="CASCADE"))
    tipo = Column(Enum('café da manhã', 'almoço', 'lanche', 'jantar'), nullable=False)
    alimentos = Column(Text, nullable=False)

    dieta_personalizada = relationship("DietaPersonalizada", back_populates="refeicoes")

    def __init__(self, dieta_personalizada_id, tipo, alimentos):
        self.dieta_personalizada_id = dieta_personalizada_id
        self.tipo = tipo
        self.alimentos = alimentos
