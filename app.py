from api import create_app
from flask import Flask, make_response, request, jsonify
from api.validators.userValidator import User_validator
from api.models.user import User
from api.validators.errors import Bad_format_of_data
from api.utils.db import db

app= create_app()

if __name__=="__main__":
    appctx=app.app_context()
    appctx.push()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
