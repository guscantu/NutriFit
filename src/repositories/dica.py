from src.entities.dica import Dica
from src.entities.base import db

def get_lista_dicas():
    return db.session.query(Dica).all()

def get_dica(dica_id: int):
    return db.session.query(Dica).get(dica_id)

def add_dica(objetivo: str, texto: str):
    objetivos_validos = ['perder peso', 'ganhar massa muscular', 'manter peso']
    if objetivo not in objetivos_validos:
        raise ValueError("Objetivo inválido para a dica.")
    
    dica = Dica(objetivo=objetivo, texto=texto)
    db.session.add(dica)
    db.session.commit()
    return dica

def update_dica(dica_id: int, objetivo: str = None, texto: str = None):
    dica = db.session.query(Dica).get(dica_id)
    if not dica:
        raise Exception("Dica não encontrada.")
    if objetivo is not None:
        objetivos_validos = ['perder peso', 'ganhar massa muscular', 'manter peso']
        if objetivo not in objetivos_validos:
            raise ValueError("Objetivo inválido para a dica.")
        dica.objetivo = objetivo
    if texto is not None:
        dica.texto = texto
    db.session.commit()
    return dica

def delete_dica(dica_id: int):
    dica = db.session.query(Dica).get(dica_id)
    if not dica:
        raise Exception("Dica não encontrada.")
    db.session.delete(dica)
    db.session.commit()
    return dica
