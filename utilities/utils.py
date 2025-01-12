from typing import Type
from models.base import T
from models.user import UserModel


def find_or_404(Model: Type["T"], message: str = "item not present", **kwargs):
    def wrapper(func):
        def inner(*func_args, **func_kwargs):
            item = Model.find_one(**kwargs)
            item: Type["T"]
            if not item:
                return {"message": message, "class": Model.__qualname__}, 404
            return func(*func_args, item, **func_kwargs)

        return inner

    return wrapper


def if_exist_400(Model: Type["T"], message: str = "item already exist", **kwargs):
    def wrapper(func):
        def inner(*func_args, **func_kwargs):
            item = Model.find_one(**kwargs)
            if item:
                return {"message": message, "class": Model.__qualname__}, 400
            return func(*func_args, **func_kwargs)

        return inner

    return wrapper


def user_logged_in(**kwargs):
    return find_or_404(UserModel, message="please login again", **kwargs)


def admin_operation(**kwargs):
    def wrapper(func):
        def inner(*func_args, **func_kwargs):
            item = UserModel.find_one(**kwargs)
            item: UserModel
            if not item:
                return {"message": "please login again"}, 404
            if item.role.lower() != "admin":
                return {"message": "you are not allowed to perform this operation"}, 403
            return func(*func_args, **func_kwargs)

        return inner

    return wrapper
