from flask import Flask
from flask_restful import Api
from src.entities.base import db
from src.routes.endpoint import initialize_endpoints

def create_app() -> Flask:
    app = Flask(__name__)

    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Bmw4632%40@localhost:3306/NutriFitBanco'


    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa o banco de dados
    db.init_app(app)

    # Inicializa a API com o prefixo /api
    api = Api(app, prefix="/api")

    # Inicializa os endpoints (rotas)
    initialize_endpoints (api)

    return app
