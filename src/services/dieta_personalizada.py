from src.repositories.dieta_personalizada import get_dietas_personalizadas, get_dieta_personalizada, add_dieta_personalizada, update_dieta_personalizada, delete_dieta_personalizada
from marshmallow import ValidationError

def getDietasPersonalizadas():
    return get_dietas_personalizadas()

def getDietaPersonalizada(dieta_id: int):
    return get_dieta_personalizada(dieta_id)

def addDietaPersonalizada(faixa_peso_id: int, faixa_altura_id: int, faixa_idade_id: int, objetivo: str, restricao: str, descricao: str):
    if objetivo not in ['perder peso', 'ganhar massa muscular', 'manter peso']:
        raise ValidationError("Objetivo inválido.")
    return add_dieta_personalizada(faixa_peso_id, faixa_altura_id, faixa_idade_id, objetivo, restricao, descricao)

def updateDietaPersonalizada(dieta_id: int, **kwargs):
    return update_dieta_personalizada(dieta_id, **kwargs)

def deleteDietaPersonalizada(dieta_id: int):
    return delete_dieta_personalizada(dieta_id)
