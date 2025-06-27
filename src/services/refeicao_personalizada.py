from src.repositories.refeicao_personalizada import (
    get_refeicoes_personalizadas,
    get_refeicao_personalizada,
    add_refeicao_personalizada,
    update_refeicao_personalizada,
    delete_refeicao_personalizada,
    RefeicaoPersonalizadaNotFound
)
from marshmallow import ValidationError

VALID_TIPOS = ['café da manhã', 'almoço', 'lanche', 'jantar']

def getRefeicoesPersonalizadas():
    return get_refeicoes_personalizadas()

def getRefeicaoPersonalizada(refeicao_id: int):
    return get_refeicao_personalizada(refeicao_id)

def addRefeicaoPersonalizada(dieta_personalizada_id: int, tipo: str, alimentos: str):
    if tipo not in VALID_TIPOS:
        raise ValidationError("Tipo de refeição inválido.")
    if not alimentos or alimentos.strip() == "":
        raise ValidationError("Campo alimentos é obrigatório.")
    return add_refeicao_personalizada(dieta_personalizada_id, tipo, alimentos)

def updateRefeicaoPersonalizada(refeicao_id: int, **kwargs):
    if 'tipo' in kwargs and kwargs['tipo'] not in VALID_TIPOS:
        raise ValidationError("Tipo de refeição inválido.")
    if 'alimentos' in kwargs and (not kwargs['alimentos'] or kwargs['alimentos'].strip() == ""):
        raise ValidationError("Campo alimentos é obrigatório.")
    try:
        return update_refeicao_personalizada(refeicao_id, **kwargs)
    except RefeicaoPersonalizadaNotFound as e:
        raise ValidationError(str(e))

def deleteRefeicaoPersonalizada(refeicao_id: int):
    return delete_refeicao_personalizada(refeicao_id)
