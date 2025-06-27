from flask_restful import Resource, abort
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields, ValidationError
from src.services.substituicao_alimentar import (
    getSubstituicoes,
    getSubstituicao,
    addSubstituicao,
    updateSubstituicao,
    deleteSubstituicao,
)

class SubstituicaoAlimentoResponseSchema(Schema):
    id = fields.Int()
    restricao_id = fields.Int()
    alimento_original = fields.Str()
    alimento_substituto = fields.Str()

class SubstituicaoAlimentoRequestSchema(Schema):
    restricao_id = fields.Int(required=True)
    alimento_original = fields.Str(required=True)
    alimento_substituto = fields.Str(required=True)

class SubstituicaoAlimentoItem(MethodResource, Resource):
    @marshal_with(SubstituicaoAlimentoResponseSchema)
    def get(self, substituicao_id):
        substituicao = getSubstituicao(substituicao_id)
        if not substituicao:
            abort(404, message="Substituição não encontrada")
        return substituicao

    @use_kwargs(SubstituicaoAlimentoRequestSchema, location="json")
    @marshal_with(SubstituicaoAlimentoResponseSchema)
    def put(self, substituicao_id, **kwargs):
        try:
            substituicao = updateSubstituicao(substituicao_id, **kwargs)
            return substituicao
        except ValidationError as e:
            abort(400, message=str(e))

    def delete(self, substituicao_id):
        try:
            deleteSubstituicao(substituicao_id)
            return '', 204
        except ValidationError as e:
            abort(404, message=str(e))

class SubstituicaoAlimentoList(MethodResource, Resource):
    @marshal_with(SubstituicaoAlimentoResponseSchema(many=True))
    def get(self):
        return getSubstituicoes()

    @use_kwargs(SubstituicaoAlimentoRequestSchema, location="json")
    @marshal_with(SubstituicaoAlimentoResponseSchema)
    def post(self, **kwargs):
        try:
            substituicao = addSubstituicao(**kwargs)
            return substituicao, 201
        except ValidationError as e:
            abort(400, message=str(e))
