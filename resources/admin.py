from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.category import CategoryModel
from utilities.utils import admin_operation, if_exist_400, find_or_404


class CategoryResource(Resource):
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True)
        payload = parser.parse_args()
        name = payload["name"]

        @admin_operation(username=get_jwt_identity())
        @if_exist_400(CategoryModel, message=f"'{name}' already exist", name=name)
        def inner():
            category = CategoryModel(name=name)
            category.save()
            return {"message": f"category '{name}' created", "data": category.json()}

        return inner()


class SpecificCategoryResource(Resource):
    @jwt_required()
    def put(self, category_id):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True)
        payload = parser.parse_args()
        name = payload["name"]

        @admin_operation(username=get_jwt_identity())
        @find_or_404(CategoryModel, message=f"category with id '{category_id}' not found", id=category_id)
        def inner(*args):
            (category,) = args
            category: CategoryModel
            duplicate_category = CategoryModel.find_one(name=name)
            if duplicate_category and duplicate_category.id != category.id:
                return {"message": f"category '{name}' already exist"}, 400

            category.name = name
            category.save()
            return {"message": f"category updated", "data": category.json()}

        return inner()

    @jwt_required()
    def delete(self, category_id):
        @admin_operation(username=get_jwt_identity())
        @find_or_404(CategoryModel, message=f"category with '{category_id}' not found", id=category_id)
        def inner(*args):
            (category,) = args
            category: CategoryModel
            category.delete()
            return {"message": f"category '{category.name}' deleted"}, 200

        return inner()
