from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import UserModel
from models.cart import CartModel
from models.product import ProductModel
from utilities.utils import user_logged_in, find_or_404, if_exist_400


class UserAccountResource(Resource):
    @jwt_required()
    def get(self):
        @user_logged_in(id=get_jwt_identity())
        def inner(*args):
            return [user.json() for user in UserModel.find_all()]

        return inner()

    @jwt_required()
    def delete(self):
        @user_logged_in(id=get_jwt_identity())
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

        @user_logged_in(id=get_jwt_identity())
        def inner(*args):
            (logged_user,) = args
            logged_user: UserModel
            logged_user.password = password
            logged_user.save()

            return {"message": "user details has been updated", "data": logged_user.json()}, 200

        return inner()


class UserCartResource(Resource):
    @jwt_required()
    def get(self):
        @user_logged_in(id=get_jwt_identity())
        def inner(*args):
            (logged_user,) = args
            logged_user: UserModel
            carts = CartModel.find_all(user=logged_user)
            return [cart.json() for cart in carts]

        return inner()


class UserSpecificCartResource(Resource):
    @jwt_required()
    def post(self, product_id):
        qty = 1

        @user_logged_in(id=get_jwt_identity())
        @find_or_404(ProductModel, id=product_id)
        @if_exist_400(CartModel, user_id=get_jwt_identity(), product_id=product_id)
        def inner(*args):
            cart = CartModel(user_id=get_jwt_identity(), product_id=product_id, qty=qty)
            cart.save()
            return {"message": "item added to cart", "data": cart.json()}

        return inner()

    @jwt_required()
    def put(self, product_id):
        parser = reqparse.RequestParser()
        parser.add_argument("qty", type=int, required=True)
        qty = parser.parse_args()["qty"]
        if qty <= 0:
            return {"message": "invalid qty"}, 400

        @user_logged_in(id=get_jwt_identity())
        @find_or_404(CartModel, user_id=get_jwt_identity(), product_id=product_id)
        def inner(*args):
            (_, cart) = args
            cart: CartModel
            cart.qty = qty
            cart.save()
            return {"message": "item updated", "data": cart.json()}, 200

        return inner()

    @jwt_required()
    def delete(self, product_id):
        @user_logged_in(id=get_jwt_identity())
        @find_or_404(CartModel, user_id=get_jwt_identity(), product_id=product_id)
        def inner(*args):
            (_, cart) = args
            cart: CartModel
            cart_data = cart.json()
            cart.delete()
            return {"message": "item deleted", "data": cart_data}, 200

        return inner()
