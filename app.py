from flask import Flask
from flask_restful import Api
from src.init import create_app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
