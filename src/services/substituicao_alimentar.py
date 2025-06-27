from src.repositories.substituicao_alimentar import (
    get_substituicoes,
    get_substituicao,
    add_substituicao,
    update_substituicao,
    delete_substituicao,
    SubstituicaoNotFound
)
from marshmallow import ValidationError

def getSubstituicoes():
    return get_substituicoes()

def getSubstituicao(substituicao_id: int):
    return get_substituicao(substituicao_id)

def addSubstituicao(restricao_id: int, alimento_original: str, alimento_substituto: str):
    if not alimento_original or not alimento_substituto:
        raise ValidationError("Alimentos não podem ser vazios.")
    return add_substituicao(restricao_id, alimento_original.strip(), alimento_substituto.strip())

def updateSubstituicao(substituicao_id: int, restricao_id: int = None, alimento_original: str = None, alimento_substituto: str = None):
    try:
        return update_substituicao(substituicao_id, restricao_id, alimento_original, alimento_substituto)
    except SubstituicaoNotFound as e:
        raise ValidationError(str(e))

def deleteSubstituicao(substituicao_id: int):
    try:
        return delete_substituicao(substituicao_id)
    except SubstituicaoNotFound as e:
        raise ValidationError(str(e))
