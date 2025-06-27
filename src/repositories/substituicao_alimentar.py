from src.entities.substituicao_alimentar import SubstituicaoAlimento
from src.entities.base import db

class SubstituicaoNotFound(Exception):
    pass

def get_substituicoes():
    return db.session.query(SubstituicaoAlimento).all()

def get_substituicao(substituicao_id):
    return db.session.query(SubstituicaoAlimento).get(substituicao_id)

def add_substituicao(restricao_id: int, alimento_original: str, alimento_substituto: str):
    sub = SubstituicaoAlimento(
        restricao_id=restricao_id,
        alimento_original=alimento_original,
        alimento_substituto=alimento_substituto
    )
    db.session.add(sub)
    db.session.commit()
    return sub

def update_substituicao(substituicao_id: int, restricao_id: int = None, alimento_original: str = None, alimento_substituto: str = None):
    sub = db.session.query(SubstituicaoAlimento).get(substituicao_id)
    if not sub:
        raise SubstituicaoNotFound("Substituição não encontrada.")

    if restricao_id is not None:
        sub.restricao_id = restricao_id
    if alimento_original is not None:
        sub.alimento_original = alimento_original
    if alimento_substituto is not None:
        sub.alimento_substituto = alimento_substituto

    db.session.commit()
    return sub

def delete_substituicao(substituicao_id):
    sub = db.session.query(SubstituicaoAlimento).get(substituicao_id)
    if not sub:
        raise SubstituicaoNotFound("Substituição não encontrada.")
    db.session.delete(sub)
    db.session.commit()
    return sub
