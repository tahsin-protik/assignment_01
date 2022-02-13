from flask import Flask
from .utils.db import db
from .main import setRoutes

def create_app(config="Dev"):
    database_uri="sqlite:///database"
    if config=="testing":
        database_uri="sqlite://"
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]=database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True
    db.init_app(app)
    setRoutes(app)

    return app


