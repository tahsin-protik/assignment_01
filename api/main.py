from flask import Flask, make_response, request, jsonify
from .validators.userValidator import User_validator
from .models.user import User
from .validators.errors import Bad_format_of_data
from .utils.db import db

def setRoutes(app):
    @app.route('/')
    def home():
        return "Hello"

    @app.route('/create', methods=['POST'])
    def create():
        try:
            args=request.json
            User_validator(args)

            new_user= User(username=args.get('username', None),
            first_name=args.get('first_name', None),
            last_name=args.get('last_name', None),
            user_type=args.get('user_type', None),
            street= args.get('street', None),
            city=args.get('city', None),
            state=args.get('state', None),
            zip_code= args.get('zip_code', None),
            parent= args.get('parent', None))

            try:
                db.session.add(new_user)
                db.session.commit()
            except Exception as e:
                response=make_response(jsonify({"message": "Service Unavailable"}), 500)
                return response
            new_user=new_user.as_dict()
            response=make_response(jsonify({"message": "User Created", "payload": new_user}), 200)
            return response
        except Bad_format_of_data as e:
            response=make_response(jsonify({"message": e.message}), e.status)
            return response

    @app.route('/delete/<username>', methods=['DELETE'])
    def delete(username):
        
        try:
            print(username)
            user=User.query.filter_by(username=username).delete()
            if not user:
                raise Bad_format_of_data(404, "User Not Found")
            try:
                db.session.commit()
            except:
                response=make_response(jsonify({"message": "Service Unavailable"}), 500)
                return response

            response=make_response(jsonify({"message": "User Deleted"}), 200)
            return response
        except Bad_format_of_data as e:
            response=make_response(jsonify({"message": e.message}), e.status)
            return response

    @app.route('/update', methods=['POST'])
    def update():
        try:
            args=request.json
            
            try:
                user=User.query.filter_by(username=args["username"]).first()
            except:
                response=make_response(jsonify({"message": "Service Unavailable"}), 500)
                return response
            
            if not user:
                raise Bad_format_of_data(400, "User Doesn't Exist")

            args['user_type']=user.user_type
            args['parent']=user.parent

            args['first_name']= args.get('first_name') if args.get('first_name', None) else user.first_name
            args['last_name']= args.get('last_name') if args.get('last_name', None) else user.last_name
            
            args['street']= args.get('street') if args.get('street', None) else user.street
            args['city']= args.get('city') if args.get('city', None) else user.city
            args['state']= args.get('state') if args.get('state', None) else user.state
            args['zip_code']= args.get('zip_code') if args.get('zip_code', None) else user.zip_code

            User_validator(args, "update")

            user.first_name=args.get('first_name', None)
            user.last_name=args.get('last_name', None)
            user.street= args.get('street', None)
            user.city=args.get('city', None)
            user.state=args.get('state', None)
            user.zip_code= args.get('zip_code', None)

            try:
                db.session.commit()
            except:
                response=make_response(jsonify({"message": "Service Unavailable"}), 500)
                return response
            user=user.as_dict()
            response=make_response(jsonify({"message": "User Updated", "payload": user}), 200)
            return response

        except Bad_format_of_data as e:
            response=make_response(jsonify({"message": e.message}), e.status)
            return response


    @app.route('/users', methods=['GET'])
    def getAll():
        try:
            users=User.query.all()
        except:
            response=make_response(jsonify({"message": "Service Unavailable"}), 500)
            return response
        for x in users:
            x=x.as_dict()
        response=make_response(jsonify({"message": "User List", "payload": users}), 200)
        return response