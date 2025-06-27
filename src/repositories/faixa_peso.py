from src.entities.faixapeso import FaixaPeso
from src.entities.base import db

def get_faixas_peso():
    return db.session.query(FaixaPeso).all()

def get_faixa_peso(faixa_id):
    return db.session.get(FaixaPeso, faixa_id)

def add_faixa_peso(faixa_min: float, faixa_max: float):
    faixa = FaixaPeso(faixa_min=faixa_min, faixa_max=faixa_max)
    db.session.add(faixa)
    db.session.commit()
    return faixa

def update_faixa_peso(faixa_id: int, faixa_min: float = None, faixa_max: float = None):
    faixa = db.session.get(FaixaPeso, faixa_id)
    if not faixa:
        raise Exception("Faixa de peso não encontrada")
    if faixa_min is not None:
        faixa.faixa_min = faixa_min
    if faixa_max is not None:
        faixa.faixa_max = faixa_max
    db.session.commit()
    return faixa

def delete_faixa_peso(faixa_id):
    faixa = db.session.get(FaixaPeso, faixa_id)
    if faixa:
        db.session.delete(faixa)
        db.session.commit()
    return faixa
