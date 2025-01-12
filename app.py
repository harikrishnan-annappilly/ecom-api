from flask import Flask, Blueprint
from flask_jwt_extended import JWTManager
from flask_restful import Api
from datetime import timedelta

from db import db
from resources.user import UserResource, RegisterResource, LoginResource

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
api.add_resource(UserResource, "/users")

# Auth Resources
api.add_resource(RegisterResource, "/auth/register")
api.add_resource(LoginResource, "/auth/login")

# Admin Resources

# User Resources


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
