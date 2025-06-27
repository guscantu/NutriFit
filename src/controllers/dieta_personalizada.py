from flask_restful import Resource
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields
from src.services.dieta_personalizada import getDietasPersonalizadas, getDietaPersonalizada, addDietaPersonalizada, updateDietaPersonalizada, deleteDietaPersonalizada

class DietaPersonalizadaResponseSchema(Schema):
    id = fields.Int()
    faixa_peso_id = fields.Int()
    faixa_altura_id = fields.Int()
    faixa_idade_id = fields.Int()
    objetivo = fields.Str()
    restricao = fields.Str()
    descricao = fields.Str()

class DietaPersonalizadaRequestSchema(Schema):
    faixa_peso_id = fields.Int(required=True)
    faixa_altura_id = fields.Int(required=True)
    faixa_idade_id = fields.Int(required=True)
    objetivo = fields.Str(required=True)
    restricao = fields.Str()
    descricao = fields.Str(required=True)

class DietaPersonalizadaItem(MethodResource, Resource):
    @marshal_with(DietaPersonalizadaResponseSchema)
    def get(self, dieta_personalizada_id):
        return getDietaPersonalizada(dieta_personalizada_id)

    @use_kwargs(DietaPersonalizadaRequestSchema, location="form")
    @marshal_with(DietaPersonalizadaResponseSchema)
    def put(self, dieta_personalizada_id, **kwargs):
        return updateDietaPersonalizada(dieta_personalizada_id, **kwargs)

    def delete(self, dieta_personalizada_id):
        deleteDietaPersonalizada(dieta_personalizada_id)
        return '', 204

class DietaPersonalizadaList(MethodResource, Resource):
    @marshal_with(DietaPersonalizadaResponseSchema(many=True))
    def get(self):
        return getDietasPersonalizadas()

    @use_kwargs(DietaPersonalizadaRequestSchema, location="form")
    @marshal_with(DietaPersonalizadaResponseSchema)
    def post(self, **kwargs):
        return addDietaPersonalizada(**kwargs), 201
