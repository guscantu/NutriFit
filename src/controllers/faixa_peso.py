from flask_restful import Resource
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields
from src.services.faixa_peso import getFaixasPeso, getFaixaPeso, addFaixaPeso, updateFaixaPeso, deleteFaixaPeso

class FaixaPesoResponseSchema(Schema):
    id = fields.Int()
    faixa_min = fields.Float()
    faixa_max = fields.Float()

class FaixaPesoRequestSchema(Schema):
    faixa_min = fields.Float(required=True)
    faixa_max = fields.Float(required=True)

class FaixaPesoItem(MethodResource, Resource):
    @marshal_with(FaixaPesoResponseSchema)
    def get(self, faixa_peso_id):
        return getFaixaPeso(faixa_peso_id)

    @use_kwargs(FaixaPesoRequestSchema, location="json")
    @marshal_with(FaixaPesoResponseSchema)
    def put(self, faixa_peso_id, **kwargs):
        return updateFaixaPeso(faixa_peso_id, **kwargs)

    def delete(self, faixa_peso_id):
        deleteFaixaPeso(faixa_peso_id)
        return '', 204

class FaixaPesoList(MethodResource, Resource):
    @marshal_with(FaixaPesoResponseSchema(many=True))
    def get(self):
        return getFaixasPeso()

    @use_kwargs(FaixaPesoRequestSchema, location="json")
    @marshal_with(FaixaPesoResponseSchema)
    def post(self, **kwargs):
        return addFaixaPeso(**kwargs), 201
