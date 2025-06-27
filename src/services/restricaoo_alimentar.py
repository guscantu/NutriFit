from src.repositories.restricao_alimentar import (
    get_lista_restricoes,
    get_restricao,
    add_restricao,
    update_restricao,
    delete_restricao,
    RestricaoAlimentarNotFound
)
from marshmallow import ValidationError

def getRestricoes():
    return get_lista_restricoes()

def getRestricao(restricao_id: int):
    return get_restricao(restricao_id)

def addRestricao(nome: str):
    if not nome or not nome.strip():
        raise ValidationError("Nome da restrição é obrigatório.")
    return add_restricao(nome.strip())

def updateRestricao(restricao_id: int, nome: str = None):
    if nome is None or not nome.strip():
        raise ValidationError("Nome da restrição é obrigatório para atualização.")
    try:
        return update_restricao(restricao_id, nome.strip())
    except RestricaoAlimentarNotFound as e:
        raise ValidationError(str(e))

def deleteRestricao(restricao_id: int):
    try:
        return delete_restricao(restricao_id)
    except RestricaoAlimentarNotFound as e:
        raise ValidationError(str(e))
