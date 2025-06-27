from sqlalchemy import Column, Integer, String, ForeignKey
from src.entities.base import Base

class SubstituicaoAlimento(Base):
    __tablename__ = "substituicaoalimento"

    id = Column(Integer, primary_key=True, autoincrement=True)
    restricao_id = Column(Integer, ForeignKey("restricaoalimentar.id", ondelete="CASCADE"))
    alimento_original = Column(String(100), nullable=False)
    alimento_substituto = Column(String(100), nullable=False)

    def __init__(self, restricao_id, alimento_original, alimento_substituto):
        self.restricao_id = restricao_id
        self.alimento_original = alimento_original
        self.alimento_substituto = alimento_substituto
