from flask_restful import Resource, abort
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields
from src.services.progresso import getProgresso, getProgressoById, addProgresso, updateProgresso, deleteProgresso

class ProgressoResponseSchema(Schema):
    id = fields.Int()
    usuario_id = fields.Int()
    dataprogresso = fields.Date()
    peso = fields.Float()
    imc = fields.Float()

class ProgressoRequestSchema(Schema):
    usuario_id = fields.Int(required=True)
    dataprogresso = fields.Date(required=True)
    peso = fields.Float(required=True)
    imc = fields.Float()

class ProgressoItem(MethodResource, Resource):
    @marshal_with(ProgressoResponseSchema)
    def get(self, progresso_id):
        progresso = getProgressoById(progresso_id)
        if not progresso:
            abort(404, message="Progresso não encontrado.")
        return progresso

    @use_kwargs(ProgressoRequestSchema, location="form")
    @marshal_with(ProgressoResponseSchema)
    def put(self, progresso_id, **kwargs):
        return updateProgresso(progresso_id, **kwargs)

    def delete(self, progresso_id):
        deleteProgresso(progresso_id)
        return '', 204

class ProgressoList(MethodResource, Resource):
    @marshal_with(ProgressoResponseSchema(many=True))
    def get(self):
        return getProgresso()

    @use_kwargs(ProgressoRequestSchema, location="form")
    @marshal_with(ProgressoResponseSchema)
    def post(self, **kwargs):
        return addProgresso(**kwargs), 201
