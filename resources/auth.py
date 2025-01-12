from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import UserModel


class RegisterResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("password", type=str, required=True)
        parser.add_argument("role", type=str, required=False)
        payload = parser.parse_args()
        username = payload["username"]

        if UserModel.find_one(username=username):
            return {"message": f"{username} already taken"}, 400

        user = UserModel(**payload)
        user.save()
        return {"message": f"user created - {username}", "data": user.json()}, 201


class LoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("password", type=str, required=True)
        payload = parser.parse_args()
        username = payload["username"]
        password = payload["password"]

        user = UserModel.find_one(username=username)
        if not user:
            return {"message": f"user not found - {username}"}, 404
        if user.password != password:
            return {"message": "incorrect password"}, 400

        access_token = create_access_token(identity=username, additional_claims=user.json())
        refresh_token = create_refresh_token(identity=username, additional_claims=user.json())
        return {"message": "login success!", "access_token": access_token, "refresh_token": refresh_token}, 200
