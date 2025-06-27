from src.repositories.faixa_idade import get_faixas_idade, get_faixa_idade, add_faixa_idade, update_faixa_idade, delete_faixa_idade
from marshmallow import ValidationError

def getFaixasIdade():
    return get_faixas_idade()

def getFaixaIdade(faixa_id: int):
    return get_faixa_idade(faixa_id)

def addFaixaIdade(faixa_min: int, faixa_max: int):
    if faixa_min >= faixa_max:
        raise ValidationError("Faixa mínima deve ser menor que a máxima.")
    return add_faixa_idade(faixa_min, faixa_max)

def updateFaixaIdade(faixa_id: int, faixa_min: int = None, faixa_max: int = None):
    if faixa_min is not None and faixa_max is not None and faixa_min >= faixa_max:
        raise ValidationError("Faixa mínima deve ser menor que a máxima.")
    return update_faixa_idade(faixa_id, faixa_min, faixa_max)

def deleteFaixaIdade(faixa_id: int):
    return delete_faixa_idade(faixa_id)
