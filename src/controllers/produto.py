from flask_restful import Resource
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields
from src.services.produto import getProdutos, getProduto, addProduto, updateProduto, deleteProduto

class ProdutoResponseSchema(Schema):
    id = fields.Int()
    nome = fields.Str()
    descricao = fields.Str()
    preco = fields.Float()
    link_compra = fields.Str()

class ProdutoRequestSchema(Schema):
    nome = fields.Str(required=True)
    descricao = fields.Str()
    preco = fields.Float()
    link_compra = fields.Str()

class ProdutoItem(MethodResource, Resource):
    @marshal_with(ProdutoResponseSchema)
    def get(self, produto_id):
        return getProduto(produto_id)

    @use_kwargs(ProdutoRequestSchema, location="form")
    @marshal_with(ProdutoResponseSchema)
    def put(self, produto_id, **kwargs):
        return updateProduto(produto_id, **kwargs)

    def delete(self, produto_id):
        deleteProduto(produto_id)
        return '', 204

class ProdutoList(MethodResource, Resource):
    @marshal_with(ProdutoResponseSchema(many=True))
    def get(self):
        return getProdutos()

    @use_kwargs(ProdutoRequestSchema, location="form")
    @marshal_with(ProdutoResponseSchema)
    def post(self, **kwargs):
        return addProduto(**kwargs), 201
