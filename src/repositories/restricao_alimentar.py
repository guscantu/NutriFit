from src.entities.restricao_alimentar import RestricaoAlimentar
from src.entities.base import db

class RestricaoAlimentarNotFound(Exception):
    pass

def get_lista_restricoes():
    return db.session.query(RestricaoAlimentar).all()

def get_restricao(restricao_id: int):
    return db.session.query(RestricaoAlimentar).get(restricao_id)

def add_restricao(nome: str):
    restricao = RestricaoAlimentar(nome=nome)
    db.session.add(restricao)
    db.session.commit()
    return restricao

def update_restricao(restricao_id: int, nome: str):
    restricao = db.session.query(RestricaoAlimentar).get(restricao_id)
    if not restricao:
        raise RestricaoAlimentarNotFound("Restrição alimentar não encontrada.")
    restricao.nome = nome
    db.session.commit()
    return restricao

def delete_restricao(restricao_id: int):
    restricao = db.session.query(RestricaoAlimentar).get(restricao_id)
    if not restricao:
        raise RestricaoAlimentarNotFound("Restrição alimentar não encontrada.")
    db.session.delete(restricao)
    db.session.commit()
    return restricao
