from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from models.user import UserModel


class UserResource(Resource):
    @jwt_required()
    def get(self):
        logged_user = UserModel.find_one(username=get_jwt_identity())
        if not logged_user:
            return {"message": "please login again"}, 403

        return [user.json() for user in UserModel.find_all()]

    @jwt_required()
    def delete(self):
        logged_user = UserModel.find_one(username=get_jwt_identity())
        if not logged_user:
            return {"message": "please login again"}, 403

        logged_user.delete()
        return {"message": f"user {logged_user.username} deleted"}, 200

    @jwt_required()
    def put(self):
        logged_user = UserModel.find_one(username=get_jwt_identity())
        if not logged_user:
            return {"message": "please login again"}, 403

        parser = reqparse.RequestParser()
        parser.add_argument("password", type=str, required=True)
        payload = parser.parse_args()

        logged_user.password = payload["password"]
        logged_user.save()

        return {"message": "user details has been updated", "data": logged_user.json()}, 200


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
