from src.repositories.faixa_peso import get_faixas_peso, get_faixa_peso, add_faixa_peso, update_faixa_peso, delete_faixa_peso
from marshmallow import ValidationError

def getFaixasPeso():
    return get_faixas_peso()

def getFaixaPeso(faixa_id: int):
    return get_faixa_peso(faixa_id)

def addFaixaPeso(faixa_min: float, faixa_max: float):
    if faixa_min >= faixa_max:
        raise ValidationError("Faixa mínima deve ser menor que a máxima.")
    return add_faixa_peso(faixa_min, faixa_max)

def updateFaixaPeso(faixa_id: int, faixa_min: float = None, faixa_max: float = None):
    if faixa_min is not None and faixa_max is not None and faixa_min >= faixa_max:
        raise ValidationError("Faixa mínima deve ser menor que a máxima.")
    return update_faixa_peso(faixa_id, faixa_min, faixa_max)

def deleteFaixaPeso(faixa_id: int):
    return delete_faixa_peso(faixa_id)
