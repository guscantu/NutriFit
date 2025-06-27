from sqlalchemy import text
from src.entities.usuario_restricao import Usuario_Restricao
from src.entities.base import db

def add_usuario_restricao(usuario_id: int, restricao_id: int):
    sql = text("INSERT INTO usuario_restricao (usuario_id, restricao_id) VALUES (:usuario_id, :restricao_id)")
    db.session.execute(sql, {'usuario_id': usuario_id, 'restricao_id': restricao_id})
    db.session.commit()
    return {"message": "Restrição adicionada ao usuário com sucesso."}

def delete_usuario_restricao(usuario_id: int, restricao_id: int):
    sql = text("DELETE FROM usuario_restricao WHERE usuario_id = :usuario_id AND restricao_id = :restricao_id")
    db.session.execute(sql, {'usuario_id': usuario_id, 'restricao_id': restricao_id})
    db.session.commit()
    return {"message": "Restrição removida do usuário com sucesso."}

def get_restricoes_por_usuario(usuario_id: int):
    sql = text("""
        SELECT 
            u.id AS usuario_id,
            u.nome AS usuario_nome,
            r.id AS restricao_id,
            r.nome AS restricao_nome
        FROM usuario_restricao ur
        JOIN usuario u ON u.id = ur.usuario_id
        JOIN restricaoalimentar r ON r.id = ur.restricao_id
        WHERE ur.usuario_id = :usuario_id
    """)
    result = db.session.execute(sql, {'usuario_id': usuario_id})
    rows = result.mappings().all() 


    if not rows:
        return None

    usuario_nome = rows[0]["usuario_nome"]
    restricoes = [
        {"id": row["restricao_id"], "nome": row["restricao_nome"]}
        for row in rows
    ]

    return {
        "usuario_id": usuario_id,
        "usuario_nome": usuario_nome,
        "restricoes": restricoes
    }

