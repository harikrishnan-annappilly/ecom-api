from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import UserModel
from utilities.utils import if_exist_400, find_or_404


class AuthRegisterResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("password", type=str, required=True)
        parser.add_argument("role", type=str, required=False)
        payload = parser.parse_args()
        username = payload["username"]

        @if_exist_400(UserModel, message=f"'{username}' already taken", username=username)
        def inner():
            user = UserModel(**payload)
            user.save()
            return {"message": f"user created - '{username}'", "data": user.json()}, 201

        return inner()


class AuthLoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("password", type=str, required=True)
        payload = parser.parse_args()
        username = payload["username"]
        password = payload["password"]

        @find_or_404(UserModel, message=f"'{username}' doesn't exist", username=username)
        def inner(*args):
            (user,) = args
            user: UserModel
            if user.password != password:
                return {"message": "incorrect password"}, 400

            access_token = create_access_token(identity=str(user.id), additional_claims=user.json())
            refresh_token = create_refresh_token(identity=str(user.id), additional_claims=user.json())
            return {"message": "login success!", "access_token": access_token, "refresh_token": refresh_token}, 200

        return inner()
