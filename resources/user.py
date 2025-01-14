from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.base import transaction
from models.user import UserModel
from models.cart import CartModel
from models.product import ProductModel
from models.order import OrderMainModel, OrderSubModel
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
        parser = reqparse.RequestParser()
        parser.add_argument("qty", type=int, required=True)
        qty = parser.parse_args()["qty"]

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


class UserOrdersResource(Resource):
    @jwt_required()
    def get(self):
        @user_logged_in(id=get_jwt_identity())
        def inner(*args):
            orders = OrderMainModel.find_all(user_id=get_jwt_identity())
            return [order.json() for order in orders]

        return inner()

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("address", type=str, required=True)
        address = parser.parse_args()["address"]

        @user_logged_in(id=get_jwt_identity())
        def inner(*args):
            (logged_user,) = args
            cart_items = CartModel.find_all(user=logged_user)
            if not cart_items:
                return {"message": f"nothing in cart"}, 400

            save_items, delete_items = [], []
            order_main = OrderMainModel(user=logged_user, address=address)
            grand_total = 0

            for cart_item in cart_items:
                product_id = cart_item.product_id
                qty = cart_item.qty
                price = cart_item.product.price
                total = qty * price
                grand_total += total
                order_sub = OrderSubModel(
                    order_main=order_main, product_id=product_id, qty=qty, price=price, total=total
                )
                save_items.append(order_sub)
                delete_items.append(cart_item)
            order_main.grand_total = grand_total
            save_items.append(order_main)

            if not transaction(save_items=save_items, delete_items=delete_items):
                return {"message": "something went wrong while making purchase"}, 500
            return order_main.json(), 201

        return inner()


class UserOrderResource(Resource):
    @jwt_required()
    def get(self, order_id):
        @user_logged_in(id=get_jwt_identity())
        @find_or_404(OrderMainModel, id=order_id)
        def inner(*args):
            (_, order) = args
            order: OrderMainModel
            return order.full_json(), 200

        return inner()
