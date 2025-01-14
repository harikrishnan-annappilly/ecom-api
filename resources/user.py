from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import UserModel
from utilities.utils import user_logged_in


class UserAccountResource(Resource):
    @jwt_required()
    def get(self):
        @user_logged_in(username=get_jwt_identity())
        def inner(*args):
            return [user.json() for user in UserModel.find_all()]

        return inner()

    @jwt_required()
    def delete(self):
        @user_logged_in(username=get_jwt_identity())
        def inner(*args):
            (logged_user,) = args
            logged_user: UserModel
            logged_user.delete()
            return {"message": f"user '{logged_user.username}' deleted"}, 200

        return inner()

    @jwt_required()
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("password", type=str, required=True)
        payload = parser.parse_args()
        password = payload["password"]

        @user_logged_in(username=get_jwt_identity())
        def inner(*args):
            (logged_user,) = args
            logged_user: UserModel
            logged_user.password = password
            logged_user.save()

            return {"message": "user details has been updated", "data": logged_user.json()}, 200

        return inner()
