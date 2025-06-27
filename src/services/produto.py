from src.repositories.produto import get_lista_produtos, get_produto, add_produto, update_produto, delete_produto
from marshmallow import ValidationError

def getProdutos():
    return get_lista_produtos()

def getProduto(produto_id: int):
    return get_produto(produto_id)

def addProduto(nome: str, descricao: str = None, preco: float = None, link_compra: str = None):
    if not nome:
        raise ValidationError("Nome do produto é obrigatório.")
    return add_produto(nome, descricao, preco, link_compra)

def updateProduto(produto_id: int, nome: str = None, descricao: str = None, preco: float = None, link_compra: str = None):
    return update_produto(produto_id, nome, descricao, preco, link_compra)

def deleteProduto(produto_id: int):
    return delete_produto(produto_id)
