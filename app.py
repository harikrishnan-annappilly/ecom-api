from flask import Flask, Blueprint
from flask_jwt_extended import JWTManager
from flask_restful import Api
from datetime import timedelta

from db import db
from resources.auth import AuthRegisterResource, AuthLoginResource
from resources.user import UserAccountResource
from resources.user import UserCartResource, UserSpecificCartResource
from resources.user import UserOrdersResource, UserOrderResource
from resources.common import CommonCategoriesResource, CommonProductsResource, CommonSpecificProductsResource
from resources.admin import AdminCategoryResource, AdminSpecificCategoryResource
from resources.admin import AdminProductResource, AdminSpecificProductResource

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICIATION"] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=10)


db.init_app(app)
jwt = JWTManager(app)


@app.before_request
def create_tables():
    db.create_all()


@app.route("/health")
def index():
    return "App running....", 200


# Setup API with '/api' prefix
api_bp = Blueprint("api", __name__)
api = Api(api_bp)
app.register_blueprint(api_bp, url_prefix="/api")

# Common Resources
api.add_resource(CommonCategoriesResource, "/categories")
api.add_resource(CommonProductsResource, "/products")
api.add_resource(CommonSpecificProductsResource, "/product/<int:product_id>")

# Auth Resources
api.add_resource(AuthRegisterResource, "/auth/register")
api.add_resource(AuthLoginResource, "/auth/login")

# Admin Resources
api.add_resource(AdminCategoryResource, "/admin/category")
api.add_resource(AdminSpecificCategoryResource, "/admin/category/<int:category_id>")
api.add_resource(AdminProductResource, "/admin/product")
api.add_resource(AdminSpecificProductResource, "/admin/product/<int:product_id>")

# User Resources
api.add_resource(UserAccountResource, "/users")
api.add_resource(UserCartResource, "/cart")
api.add_resource(UserSpecificCartResource, "/cart/<int:product_id>")
api.add_resource(UserOrdersResource, "/orders")
api.add_resource(UserOrderResource, "/order/<int:order_id>")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
