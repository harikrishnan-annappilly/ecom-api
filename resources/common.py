from flask_restful import Resource
from models.category import CategoryModel
from models.product import ProductModel
from utilities.utils import find_or_404


class CommonCategoriesResource(Resource):
    def get(self):
        categories = CategoryModel.find_all()
        return [category.json() for category in categories]


class CommonProductsResource(Resource):
    def get(self):
        products = ProductModel.find_all()
        return [product.json() for product in products]


class CommonSpecificProductsResource(Resource):
    def get(self, product_id):
        @find_or_404(ProductModel, message=f"product with id {product_id} not found", id=product_id)
        def inner(*args):
            (product,) = args
            product: ProductModel
            return product.json()

        return inner()
