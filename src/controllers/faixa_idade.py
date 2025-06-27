from flask_restful import Resource
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields
from src.services.faixa_idade import getFaixasIdade, getFaixaIdade, addFaixaIdade, updateFaixaIdade, deleteFaixaIdade

class FaixaIdadeResponseSchema(Schema):
    id = fields.Int()
    faixa_min = fields.Int()
    faixa_max = fields.Int()

class FaixaIdadeRequestSchema(Schema):
    faixa_min = fields.Int(required=True)
    faixa_max = fields.Int(required=True)

class FaixaIdadeItem(MethodResource, Resource):
    @marshal_with(FaixaIdadeResponseSchema)
    def get(self, faixa_idade_id):
        return getFaixaIdade(faixa_idade_id)

    @use_kwargs(FaixaIdadeRequestSchema, location="json")
    @marshal_with(FaixaIdadeResponseSchema)
    def put(self, faixa_idade_id, **kwargs):
        return updateFaixaIdade(faixa_idade_id, **kwargs)

    def delete(self, faixa_idade_id):
        deleteFaixaIdade(faixa_idade_id)
        return '', 204

class FaixaIdadeList(MethodResource, Resource):
    @marshal_with(FaixaIdadeResponseSchema(many=True))
    def get(self):
        return getFaixasIdade()

    @use_kwargs(FaixaIdadeRequestSchema, location="json")
    @marshal_with(FaixaIdadeResponseSchema)
    def post(self, **kwargs):
        return addFaixaIdade(**kwargs), 201
