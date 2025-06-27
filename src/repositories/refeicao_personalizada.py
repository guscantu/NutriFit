from src.entities.refeicaopersonalizada import RefeicaoPersonalizada
from src.entities.base import db

class RefeicaoPersonalizadaNotFound(Exception):
    pass

def get_refeicoes_personalizadas():
    return db.session.query(RefeicaoPersonalizada).all()

def get_refeicao_personalizada(refeicao_id: int):
    return db.session.query(RefeicaoPersonalizada).get(refeicao_id)

def add_refeicao_personalizada(dieta_personalizada_id: int, tipo: str, alimentos: str):
    refeicao = RefeicaoPersonalizada(dieta_personalizada_id=dieta_personalizada_id, tipo=tipo, alimentos=alimentos)
    db.session.add(refeicao)
    db.session.commit()
    return refeicao

def update_refeicao_personalizada(refeicao_id: int, dieta_personalizada_id: int = None, tipo: str = None, alimentos: str = None):
    refeicao = db.session.query(RefeicaoPersonalizada).get(refeicao_id)
    if not refeicao:
        raise RefeicaoPersonalizadaNotFound("Refeição personalizada não encontrada")

    if dieta_personalizada_id is not None:
        refeicao.dieta_personalizada_id = dieta_personalizada_id
    if tipo is not None:
        refeicao.tipo = tipo
    if alimentos is not None:
        refeicao.alimentos = alimentos

    db.session.commit()
    return refeicao

def delete_refeicao_personalizada(refeicao_id: int):
    refeicao = db.session.query(RefeicaoPersonalizada).get(refeicao_id)
    if refeicao:
        db.session.delete(refeicao)
        db.session.commit()
    return refeicao
