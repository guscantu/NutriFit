from flask_restful import Resource
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields
from src.services.refeicao_personalizada import getRefeicoesPersonalizadas, getRefeicaoPersonalizada, addRefeicaoPersonalizada, updateRefeicaoPersonalizada, deleteRefeicaoPersonalizada

class RefeicaoPersonalizadaResponseSchema(Schema):
    id = fields.Int()
    dieta_personalizada_id = fields.Int()
    tipo = fields.Str()
    alimentos = fields.Str()

class RefeicaoPersonalizadaRequestSchema(Schema):
    dieta_personalizada_id = fields.Int(required=True)
    tipo = fields.Str(required=True)
    alimentos = fields.Str(required=True)

class RefeicaoPersonalizadaItem(MethodResource, Resource):
    @marshal_with(RefeicaoPersonalizadaResponseSchema)
    def get(self, refeicao_personalizada_id):
        return getRefeicaoPersonalizada(refeicao_personalizada_id)

    @use_kwargs(RefeicaoPersonalizadaRequestSchema, location="form")
    @marshal_with(RefeicaoPersonalizadaResponseSchema)
    def put(self, refeicao_personalizada_id, **kwargs):
        return updateRefeicaoPersonalizada(refeicao_personalizada_id, **kwargs)

    def delete(self, refeicao_personalizada_id):
        deleteRefeicaoPersonalizada(refeicao_personalizada_id)
        return '', 204

class RefeicaoPersonalizadaList(MethodResource, Resource):
    @marshal_with(RefeicaoPersonalizadaResponseSchema(many=True))
    def get(self):
        return getRefeicoesPersonalizadas()

    @use_kwargs(RefeicaoPersonalizadaRequestSchema, location="form")
    @marshal_with(RefeicaoPersonalizadaResponseSchema)
    def post(self, **kwargs):
        return addRefeicaoPersonalizada(**kwargs), 201
