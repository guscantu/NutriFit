from flask_restful import Resource, abort, request
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields, validates, ValidationError
from sqlalchemy.exc import IntegrityError, OperationalError
from src.services.usuario import getUsuarios, getUsuario, addUsuario, updateUsuario, deleteUsuario

class UsuarioResponseSchema(Schema):
    id = fields.Int()
    nome = fields.Str()
    idade = fields.Int()
    peso = fields.Float()
    altura = fields.Float()
    objetivo = fields.Str()
    restricoes = fields.Str()

class UsuarioRequestSchema(Schema):
    nome = fields.Str(required=True)
    idade = fields.Int(required=True)
    peso = fields.Float(required=True)
    altura = fields.Float(required=True)
    objetivo = fields.Str(required=True)
    restricoes = fields.Str()

    @validates("objetivo")
    def validate_objetivo(self, value):
        if value not in ['perder peso', 'ganhar massa muscular', 'manter peso']:
            raise ValidationError("Objetivo inválido.")

class UsuarioItem(MethodResource, Resource):
    @marshal_with(UsuarioResponseSchema)
    def get(self, usuario_id):
        usuario = getUsuario(usuario_id)
        if not usuario:
            abort(404, message="Usuário não encontrado.")
        return usuario, 200

    @use_kwargs(UsuarioRequestSchema, location="form")
    @marshal_with(UsuarioResponseSchema)
    def put(self, usuario_id, **kwargs):
        try:
            usuario = updateUsuario(usuario_id, **kwargs)
            return usuario, 200
        except Exception as e:
            abort(400, message=str(e))

    def delete(self, usuario_id):
        usuario = deleteUsuario(usuario_id)
        if not usuario:
            abort(404, message="Usuário não encontrado.")
        return {}, 204

class UsuarioList(MethodResource, Resource):
    @marshal_with(UsuarioResponseSchema(many=True))
    def get(self):
        return getUsuarios(), 200

    @use_kwargs(UsuarioRequestSchema, location="form")
    @marshal_with(UsuarioResponseSchema)
    def post(self, **kwargs):
        try:
            usuario = addUsuario(**kwargs)
            return usuario, 201
        except ValidationError as e:
            abort(400, message=str(e))
