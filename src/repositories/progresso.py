from src.entities.progresso import Progresso
from src.entities.base import db

def get_lista_progresso():
    return db.session.query(Progresso).all()

def get_progresso(progresso_id: int):
    return db.session.query(Progresso).get(progresso_id)

def add_progresso(usuario_id: int, dataprogresso, peso: float, imc: float = None):
    progresso = Progresso(usuario_id=usuario_id, dataprogresso=dataprogresso, peso=peso, imc=imc)
    db.session.add(progresso)
    db.session.commit()
    return progresso

def update_progresso(progresso_id: int, usuario_id: int = None, dataprogresso = None, peso: float = None, imc: float = None):
    progresso = db.session.query(Progresso).get(progresso_id)
    if not progresso:
        raise Exception("Progresso não encontrado.")
    if usuario_id is not None:
        progresso.usuario_id = usuario_id
    if dataprogresso is not None:
        progresso.dataprogresso = dataprogresso
    if peso is not None:
        progresso.peso = peso
    if imc is not None:
        progresso.imc = imc
    db.session.commit()
    return progresso

def delete_progresso(progresso_id: int):
    progresso = db.session.query(Progresso).get(progresso_id)
    if not progresso:
        raise Exception("Progresso não encontrado.")
    db.session.delete(progresso)
    db.session.commit()
    return progresso
