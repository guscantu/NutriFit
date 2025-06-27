from flask_restful import Resource
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields
from src.services.faixa_altura import getFaixasAltura, getFaixaAltura, addFaixaAltura, updateFaixaAltura, deleteFaixaAltura

class FaixaAlturaResponseSchema(Schema):
    id = fields.Int()
    faixa_min = fields.Float()
    faixa_max = fields.Float()

class FaixaAlturaRequestSchema(Schema):
    faixa_min = fields.Float(required=True)
    faixa_max = fields.Float(required=True)

class FaixaAlturaItem(MethodResource, Resource):
    @marshal_with(FaixaAlturaResponseSchema)
    def get(self, faixa_altura_id):
        return getFaixaAltura(faixa_altura_id)

    @use_kwargs(FaixaAlturaRequestSchema, location="json")
    @marshal_with(FaixaAlturaResponseSchema)
    def put(self, faixa_altura_id, **kwargs):
        return updateFaixaAltura(faixa_altura_id, **kwargs)

    def delete(self, faixa_altura_id):
        deleteFaixaAltura(faixa_altura_id)
        return '', 204

class FaixaAlturaList(MethodResource, Resource):
    @marshal_with(FaixaAlturaResponseSchema(many=True))
    def get(self):
        return getFaixasAltura()

    @use_kwargs(FaixaAlturaRequestSchema, location="json")
    @marshal_with(FaixaAlturaResponseSchema)
    def post(self, **kwargs):
        return addFaixaAltura(**kwargs), 201
