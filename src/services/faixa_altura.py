from src.repositories.faixa_altura import get_faixas_altura, get_faixa_altura, add_faixa_altura, update_faixa_altura, delete_faixa_altura
from marshmallow import ValidationError

def getFaixasAltura():
    return get_faixas_altura()

def getFaixaAltura(faixa_id: int):
    return get_faixa_altura(faixa_id)

def addFaixaAltura(faixa_min: float, faixa_max: float):
    if faixa_min >= faixa_max:
        raise ValidationError("Faixa mínima deve ser menor que a máxima.")
    return add_faixa_altura(faixa_min, faixa_max)

def updateFaixaAltura(faixa_id: int, faixa_min: float = None, faixa_max: float = None):
    if faixa_min is not None and faixa_max is not None and faixa_min >= faixa_max:
        raise ValidationError("Faixa mínima deve ser menor que a máxima.")
    return update_faixa_altura(faixa_id, faixa_min, faixa_max)

def deleteFaixaAltura(faixa_id: int):
    return delete_faixa_altura(faixa_id)
