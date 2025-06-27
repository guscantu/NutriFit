from flask_restful import Resource
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields
from src.services.dica import getDicas, getDica, addDica, updateDica, deleteDica

class DicaResponseSchema(Schema):
    id = fields.Int()
    objetivo = fields.Str()
    texto = fields.Str()

class DicaRequestSchema(Schema):
    objetivo = fields.Str(required=True)
    texto = fields.Str(required=True)

class DicaItem(MethodResource, Resource):
    @marshal_with(DicaResponseSchema)
    def get(self, dica_id):
        return getDica(dica_id)

    @use_kwargs(DicaRequestSchema, location="form")
    @marshal_with(DicaResponseSchema)
    def put(self, dica_id, **kwargs):
        return updateDica(dica_id, **kwargs)

    def delete(self, dica_id):
        deleteDica(dica_id)
        return '', 204

class DicaList(MethodResource, Resource):
    @marshal_with(DicaResponseSchema(many=True))
    def get(self):
        return getDicas()

    @use_kwargs(DicaRequestSchema, location="form")
    @marshal_with(DicaResponseSchema)
    def post(self, **kwargs):
        return addDica(**kwargs), 201
