from src.repositories.progresso import get_lista_progresso, get_progresso, add_progresso, update_progresso, delete_progresso
from marshmallow import ValidationError

def getProgresso():
    return get_lista_progresso()

def getProgressoById(progresso_id: int):
    return get_progresso(progresso_id)

def addProgresso(usuario_id: int, dataprogresso, peso: float, imc: float = None):
    if peso <= 0:
        raise ValidationError("Peso deve ser maior que 0.")
    return add_progresso(usuario_id, dataprogresso, peso, imc)

def updateProgresso(progresso_id: int, usuario_id: int = None, dataprogresso = None, peso: float = None, imc: float = None):
    return update_progresso(progresso_id, usuario_id, dataprogresso, peso, imc)

def deleteProgresso(progresso_id: int):
    return delete_progresso(progresso_id)
