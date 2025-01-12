from flask_restful import Resource, reqparse
from models.category import CategoryModel


class CommonCategoriesResource(Resource):
    def get(self):
        categories = CategoryModel.find_all()
        return [category.json() for category in categories]
