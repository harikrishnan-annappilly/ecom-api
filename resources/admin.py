from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import UserModel
from models.category import CategoryModel


class CategoryResource(Resource):
    @jwt_required()
    def post(self):
        logged_user = UserModel.find_one(username=get_jwt_identity())
        if not logged_user:
            return {"message": "please login again"}, 403
        if logged_user.role.lower() != "admin":
            return {"message": "you are not allowed to perform this operation"}, 403

        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True)
        payload = parser.parse_args()
        name = payload["name"]

        if CategoryModel.find_one(name=name):
            return {"message": f"{name} already exist"}, 400

        category = CategoryModel(name=name)
        category.save()
        return {"message": f"category {name} created", "data": category.json()}


class SpecificCategoryResource(Resource):
    @jwt_required()
    def put(self, category_id):
        logged_user = UserModel.find_one(username=get_jwt_identity())
        if not logged_user:
            return {"message": "please login again"}, 403
        if logged_user.role.lower() != "admin":
            return {"message": "you are not allowed to perform this operation"}, 403

        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True)
        payload = parser.parse_args()
        name = payload["name"]

        category = CategoryModel.find_one(id=category_id)
        duplicate_category = CategoryModel.find_one(name=name)
        if not category:
            return {"message": f"category with {category_id} not found"}, 404
        if duplicate_category and duplicate_category.id != category.id:
            return {"message": f"{name} already exist"}, 400

        category.name = name
        category.save()
        return {"message": f"category updated", "data": category.json()}

    @jwt_required()
    def delete(self, category_id):
        logged_user = UserModel.find_one(username=get_jwt_identity())
        if not logged_user:
            return {"message": "please login again"}, 403
        if logged_user.role.lower() != "admin":
            return {"message": "you are not allowed to perform this operation"}, 403

        category = CategoryModel.find_one(id=category_id)
        if not category:
            return {"message": f"category with {category_id} not found"}, 404

        category.delete()
        return {"message": f"category {category.name} deleted"}, 200
