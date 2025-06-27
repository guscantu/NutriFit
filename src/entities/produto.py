from sqlalchemy import Column, Integer, String, Text, Float
from src.entities.base import Base

class Produto(Base):
    __tablename__ = "produto"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text)
    preco = Column(Float)
    link_compra = Column(String(255))

    def __init__(self, nome, descricao=None, preco=None, link_compra=None):
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.link_compra = link_compra
