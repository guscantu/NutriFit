from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.entities.base import Base

class Progresso(Base):
    __tablename__ = "progresso"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"))
    dataprogresso = Column(Date, nullable=False)
    peso = Column(Float, nullable=False)
    imc = Column(Float)

    usuario = relationship("Usuario", back_populates="progressos")

    def __init__(self, usuario_id, dataprogresso, peso, imc=None):
        self.usuario_id = usuario_id
        self.dataprogresso = dataprogresso
        self.peso = peso
        self.imc = imc
