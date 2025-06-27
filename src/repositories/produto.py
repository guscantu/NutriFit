from src.entities.produto import Produto
from src.entities.base import db

def get_lista_produtos():
    return db.session.query(Produto).all()

def get_produto(produto_id: int):
    return db.session.query(Produto).get(produto_id)

def add_produto(nome: str, descricao: str = None, preco: float = None, link_compra: str = None):
    produto = Produto(nome=nome, descricao=descricao, preco=preco, link_compra=link_compra)
    db.session.add(produto)
    db.session.commit()
    return produto

def update_produto(produto_id: int, nome: str = None, descricao: str = None, preco: float = None, link_compra: str = None):
    produto = db.session.query(Produto).get(produto_id)
    if not produto:
        raise Exception("Produto não encontrado.")
    if nome is not None:
        produto.nome = nome
    if descricao is not None:
        produto.descricao = descricao
    if preco is not None:
        produto.preco = preco
    if link_compra is not None:
        produto.link_compra = link_compra
    db.session.commit()
    return produto

def delete_produto(produto_id: int):
    produto = db.session.query(Produto).get(produto_id)
    if not produto:
        raise Exception("Produto não encontrado.")
    db.session.delete(produto)
    db.session.commit()
    return produto
