from src.repositories.dica import get_lista_dicas, get_dica, add_dica, update_dica, delete_dica
from marshmallow import ValidationError

def getDicas():
    return get_lista_dicas()

def getDica(dica_id: int):
    return get_dica(dica_id)

def addDica(objetivo: str, texto: str):
    if not texto or not objetivo:
        raise ValidationError("Objetivo e texto são obrigatórios.")
    return add_dica(objetivo, texto)

def updateDica(dica_id: int, objetivo: str = None, texto: str = None):
    return update_dica(dica_id, objetivo, texto)

def deleteDica(dica_id: int):
    return delete_dica(dica_id)
