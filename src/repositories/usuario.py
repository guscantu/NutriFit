from src.entities.usuario import Usuario
from src.entities.base import db

def get_lista_usuarios():
    """Retorna todos os usuários cadastrados."""
    return db.session.query(Usuario).all()

def get_usuario(usuario_id: int):
    """Retorna um usuário pelo ID."""
    return db.session.query(Usuario).get(usuario_id)

def add_usuario(nome: str, idade: int, peso: float, altura: float, objetivo: str, restricoes: str = None):
    """Adiciona um usuário novo após validações."""
    usuario = Usuario(
        nome=nome,
        idade=idade,
        peso=peso,
        altura=altura,
        objetivo=objetivo,
        restricoes=restricoes
    )
    db.session.add(usuario)
    db.session.commit()
    return usuario

def update_usuario(usuario_id: int, nome: str = None, idade: int = None, peso: float = None,
                   altura: float = None, objetivo: str = None, restricoes: str = None):
    """Atualiza dados do usuário."""
    usuario = db.session.query(Usuario).get(usuario_id)
    if not usuario:
        raise Exception("Usuário não encontrado.")

    if nome is not None:
        usuario.nome = nome
    if idade is not None:
        usuario.idade = idade
    if peso is not None:
        usuario.peso = peso
    if altura is not None:
        usuario.altura = altura
    if objetivo is not None:
        usuario.objetivo = objetivo
    if restricoes is not None:
        usuario.restricoes = restricoes

    db.session.commit()
    return usuario

def delete_usuario(usuario_id: int):
    """Deleta um usuário pelo ID."""
    usuario = db.session.query(Usuario).get(usuario_id)
    if not usuario:
        raise Exception("Usuário não encontrado.")
    db.session.delete(usuario)
    db.session.commit()
    return usuario
