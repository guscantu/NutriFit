from src.entities.faixaidade import FaixaIdade
from src.entities.base import db

def get_faixas_idade():
    return db.session.query(FaixaIdade).all()

def get_faixa_idade(faixa_id):
    return db.session.query(FaixaIdade).get(faixa_id)

def add_faixa_idade(faixa_min: int, faixa_max: int):
    faixa = FaixaIdade(faixa_min=faixa_min, faixa_max=faixa_max)
    db.session.add(faixa)
    db.session.commit()
    return faixa

def update_faixa_idade(faixa_id: int, faixa_min: int = None, faixa_max: int = None):
    faixa = db.session.query(FaixaIdade).get(faixa_id)
    if not faixa:
        raise Exception("Faixa de idade não encontrada")

    if faixa_min is not None:
        faixa.faixa_min = faixa_min
    if faixa_max is not None:
        faixa.faixa_max = faixa_max

    db.session.commit()
    return faixa

def delete_faixa_idade(faixa_id):
    faixa = db.session.query(FaixaIdade).get(faixa_id)
    if faixa:
        db.session.delete(faixa)
        db.session.commit()
    return faixa
