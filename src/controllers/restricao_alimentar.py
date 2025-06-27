from flask_restful import Resource
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields
from src.services.restricaoo_alimentar import getRestricoes, getRestricao, addRestricao, updateRestricao, deleteRestricao

class RestricaoResponseSchema(Schema):
    id = fields.Int()
    nome = fields.Str()

class RestricaoRequestSchema(Schema):
    nome = fields.Str(required=True)

class RestricaoItem(MethodResource, Resource):
    @marshal_with(RestricaoResponseSchema)
    def get(self, restricao_id):
        return getRestricao(restricao_id)

    @use_kwargs(RestricaoRequestSchema, location="json")
    @marshal_with(RestricaoResponseSchema)
    def put(self, restricao_id, **kwargs):
        return updateRestricao(restricao_id, **kwargs)

    def delete(self, restricao_id):
        deleteRestricao(restricao_id)
        return '', 204

class RestricaoList(MethodResource, Resource):
    @marshal_with(RestricaoResponseSchema(many=True))
    def get(self):
        return getRestricoes()

    @use_kwargs(RestricaoRequestSchema, location="json")
    @marshal_with(RestricaoResponseSchema)
    def post(self, **kwargs):
        return addRestricao(**kwargs), 201
