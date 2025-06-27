from src.repositories.usuario import get_lista_usuarios, get_usuario, add_usuario, update_usuario, delete_usuario
from marshmallow import ValidationError

def validar_dados_usuario(idade: int, peso: float, altura: float, objetivo: str):
    """Função auxiliar para validar dados de usuário."""
    if peso < 30 or peso > 200:
        raise ValidationError("Peso deve estar entre 30kg e 200kg.")
    if altura < 1.0 or altura > 2.5:
        raise ValidationError("Altura deve estar entre 1.0m e 2.5m.")
    if idade < 12 or idade > 90:
        raise ValidationError("Idade deve estar entre 12 e 90 anos.")
    if objetivo not in ['perder peso', 'ganhar massa muscular', 'manter peso']:
        raise ValidationError("Objetivo inválido.")

def getUsuarios():
    return get_lista_usuarios()

def getUsuario(usuario_id: int):
    return get_usuario(usuario_id)

def addUsuario(nome: str, idade: int, peso: float, altura: float, objetivo: str, restricoes: str = None):
    if not nome:
        raise ValidationError("Nome não pode ser vazio.")
    validar_dados_usuario(idade, peso, altura, objetivo)
    return add_usuario(nome, idade, peso, altura, objetivo, restricoes)

def updateUsuario(usuario_id: int, nome: str = None, idade: int = None, peso: float = None, 
                  altura: float = None, objetivo: str = None, restricoes: str = None):
    if any([idade, peso, altura, objetivo]):
        idade_val = idade if idade is not None else 20  # valor default apenas para validar
        peso_val = peso if peso is not None else 60
        altura_val = altura if altura is not None else 1.70
        objetivo_val = objetivo if objetivo is not None else 'manter peso'
        validar_dados_usuario(idade_val, peso_val, altura_val, objetivo_val)
    return update_usuario(usuario_id, nome, idade, peso, altura, objetivo, restricoes)

def deleteUsuario(usuario_id: int):
    return delete_usuario(usuario_id)
