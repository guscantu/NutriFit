from flask_restful import Resource, abort
from flask_apispec import use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields
from sqlalchemy.exc import IntegrityError, OperationalError
from src.services.usuario_restricao import (
    addUsuarioRestricao, deleteUsuarioRestricao, getRestricoesPorUsuario
)

class UsuarioRestricaoRequestSchema(Schema):
    usuario_id = fields.Int(required=True)
    restricao_id = fields.Int(required=True)

class UsuarioRestricaoList(MethodResource, Resource):

    @use_kwargs(UsuarioRestricaoRequestSchema, location="json")
    def post(self, usuario_id, restricao_id):
        try:
            addUsuarioRestricao(usuario_id, restricao_id)
            return {"message": "Restrição adicionada ao usuário."}, 201
        except IntegrityError as err:
            abort(500, message=str(err.__context__))
        except OperationalError as err:
            abort(500, message=str(err.__context__))

    @use_kwargs(UsuarioRestricaoRequestSchema, location="json")
    def delete(self, usuario_id, restricao_id):
        try:
            deleteUsuarioRestricao(usuario_id, restricao_id)
            return {"message": "Restrição removida do usuário."}, 204
        except OperationalError as err:
            abort(500, message=str(err.__context__))

class UsuarioRestricaoGet(MethodResource, Resource):
    def get(self, usuario_id):
        try:
            data = getRestricoesPorUsuario(usuario_id)
            if not data:
                return {"message": "Usuário não encontrado ou sem restrições."}, 404
            return data, 200
        except OperationalError as err:
            abort(500, message=str(err.__context__))


class UsuarioRestricaoDelete(MethodResource, Resource):
    def delete(self, usuario_id, restricao_id):
        try:
            deleteUsuarioRestricao(usuario_id, restricao_id)
            return {"message": "Restrição removida do usuário."}, 204
        except OperationalError as err:
            abort(500, message=str(err.__context__))
