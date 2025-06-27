from marshmallow import ValidationError
from src.repositories.usuario_restricao import (
    add_usuario_restricao,
    delete_usuario_restricao,
    get_restricoes_por_usuario
)

def addUsuarioRestricao(usuario_id: int, restricao_id: int):
    if not usuario_id or not restricao_id:
        raise ValidationError("Usuário e restrição são obrigatórios.")
    return add_usuario_restricao(usuario_id, restricao_id)

def deleteUsuarioRestricao(usuario_id: int, restricao_id: int):
    if not usuario_id or not restricao_id:
        raise ValidationError("Usuário e restrição são obrigatórios.")
    return delete_usuario_restricao(usuario_id, restricao_id)

def getRestricoesPorUsuario(usuario_id: int):
    if not usuario_id:
        raise ValidationError("Usuário é obrigatório.")
    return get_restricoes_por_usuario(usuario_id)
