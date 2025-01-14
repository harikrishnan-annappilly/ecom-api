from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.category import CategoryModel
from models.product import ProductModel
from utilities.utils import admin_operation, if_exist_400, find_or_404


class AdminCategoryResource(Resource):
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True)
        payload = parser.parse_args()
        name = payload["name"]

        @admin_operation(id=get_jwt_identity())
        @if_exist_400(CategoryModel, message=f"'{name}' already exist", name=name)
        def inner():
            category = CategoryModel(name=name)
            category.save()
            return {"message": f"category '{name}' created", "data": category.json()}

        return inner()


class AdminSpecificCategoryResource(Resource):
    @jwt_required()
    def put(self, category_id):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True)
        payload = parser.parse_args()
        name = payload["name"]

        @admin_operation(id=get_jwt_identity())
        @find_or_404(CategoryModel, message=f"category with id '{category_id}' not found", id=category_id)
        def inner(*args):
            (category,) = args
            category: CategoryModel
            if CategoryModel.find_one(not_id=category_id, name=name):
                return {"message": f"category '{name}' already exist"}, 400

            category.name = name
            category.save()
            return {"message": f"category updated", "data": category.json()}

        return inner()

    @jwt_required()
    def delete(self, category_id):
        @admin_operation(id=get_jwt_identity())
        @find_or_404(CategoryModel, message=f"category with '{category_id}' not found", id=category_id)
        def inner(*args):
            (category,) = args
            category: CategoryModel
            product_count = len(category.products)
            if product_count:
                return {
                    "message": f"category '{category.name}' is having '{product_count}' products. delete not possible."
                }, 400
            category.delete()
            return {"message": f"category '{category.name}' deleted"}, 200

        return inner()


class AdminProductResource(Resource):
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("price", type=float, required=True)
        parser.add_argument("category_id", type=int, required=True)
        payload = parser.parse_args()
        name = payload["name"]
        category_id = payload["category_id"]

        @admin_operation(id=get_jwt_identity())
        @if_exist_400(ProductModel, message=f"product '{name}' already exist", name=name)
        @find_or_404(CategoryModel, message=f"category with id '{category_id}' not found", id=category_id)
        def innner(*args):
            product = ProductModel(**payload)
            product.save()
            return {"message": f"new product created", "data": product.json()}, 201

        return innner()


class AdminSpecificProductResource(Resource):
    @jwt_required()
    def put(self, product_id):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("price", type=float, required=True)
        parser.add_argument("category_id", type=int, required=True)
        payload = parser.parse_args()
        name = payload["name"]
        price = payload["price"]
        category_id = payload["category_id"]

        @admin_operation(id=get_jwt_identity())
        @find_or_404(ProductModel, message=f"product with id '{product_id}' not found", id=product_id)
        @find_or_404(CategoryModel, message=f"category with id '{category_id}' not found", id=category_id)
        def inner(*args):
            (product, _) = args
            product: ProductModel
            if ProductModel.find_one(not_id=product_id, name=name):
                return {"message": f"product name '{name}' already exist"}, 400

            product.name = name
            product.price = price
            product.category_id = category_id
            product.save()
            return {"message": f"product '{name}' updated", "data": product.json()}, 200

        return inner()

    @jwt_required()
    def delete(self, product_id):
        @admin_operation(id=get_jwt_identity())
        @find_or_404(ProductModel, message=f"product with id '{product_id}' not found", id=product_id)
        def inner(*args):
            (product,) = args
            product: ProductModel
            product_data = product.json()
            product.delete()
            return {"message": f"product '{product.name}' deleted", "data": product_data}, 200

        return inner()
