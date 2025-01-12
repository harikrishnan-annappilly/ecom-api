from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
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
