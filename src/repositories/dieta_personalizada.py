from src.entities.dietapersonalizada import DietaPersonalizada
from src.entities.base import db

def get_dietas_personalizadas():
    return db.session.query(DietaPersonalizada).all()

def get_dieta_personalizada(dieta_id):
    return db.session.query(DietaPersonalizada).get(dieta_id)

def add_dieta_personalizada(faixa_peso_id: int, faixa_altura_id: int, faixa_idade_id: int, objetivo: str, restricao: str, descricao: str):
    dieta = DietaPersonalizada(
        faixa_peso_id=faixa_peso_id,
        faixa_altura_id=faixa_altura_id,
        faixa_idade_id=faixa_idade_id,
        objetivo=objetivo,
        restricao=restricao,
        descricao=descricao
    )
    db.session.add(dieta)
    db.session.commit()
    return dieta

def update_dieta_personalizada(dieta_id: int, faixa_peso_id: int = None, faixa_altura_id: int = None, faixa_idade_id: int = None, objetivo: str = None, restricao: str = None, descricao: str = None):
    dieta = db.session.query(DietaPersonalizada).get(dieta_id)
    if not dieta:
        raise Exception("Dieta personalizada não encontrada")

    if faixa_peso_id is not None:
        dieta.faixa_peso_id = faixa_peso_id
    if faixa_altura_id is not None:
        dieta.faixa_altura_id = faixa_altura_id
    if faixa_idade_id is not None:
        dieta.faixa_idade_id = faixa_idade_id
    if objetivo is not None:
        dieta.objetivo = objetivo
    if restricao is not None:
        dieta.restricao = restricao
    if descricao is not None:
        dieta.descricao = descricao

    db.session.commit()
    return dieta

def delete_dieta_personalizada(dieta_id):
    dieta = db.session.query(DietaPersonalizada).get(dieta_id)
    if dieta:
        db.session.delete(dieta)
        db.session.commit()
    return dieta
