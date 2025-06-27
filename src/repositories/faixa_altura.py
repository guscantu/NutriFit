from src.entities.faixaaltura import FaixaAltura
from src.entities.base import db

def get_faixas_altura():
    return db.session.query(FaixaAltura).all()

def get_faixa_altura(faixa_id):
    return db.session.query(FaixaAltura).get(faixa_id)

def add_faixa_altura(faixa_min: float, faixa_max: float):
    faixa = FaixaAltura(faixa_min=faixa_min, faixa_max=faixa_max)
    db.session.add(faixa)
    db.session.commit()
    return faixa

def update_faixa_altura(faixa_id: int, faixa_min: float = None, faixa_max: float = None):
    faixa = db.session.query(FaixaAltura).get(faixa_id)
    if not faixa:
        raise Exception("Faixa de altura não encontrada")

    if faixa_min is not None:
        faixa.faixa_min = faixa_min
    if faixa_max is not None:
        faixa.faixa_max = faixa_max

    db.session.commit()
    return faixa

def delete_faixa_altura(faixa_id):
    faixa = db.session.query(FaixaAltura).get(faixa_id)
    if faixa:
        db.session.delete(faixa)
        db.session.commit()
    return faixa
