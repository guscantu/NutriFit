from sqlalchemy import Column, Integer, ForeignKey
from src.entities.base import Base

class Usuario_Restricao(Base):
    __tablename__ = "usuario_restricao"

    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), primary_key=True)
    restricao_id = Column(Integer, ForeignKey("restricaoalimentar.id", ondelete="CASCADE"), primary_key=True)

    def __init__(self, usuario_id, restricao_id):
        self.usuario_id = usuario_id
        self.restricao_id = restricao_id
