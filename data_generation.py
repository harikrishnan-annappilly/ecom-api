from app import app
from db import db
from models.user import UserModel
from models.category import CategoryModel
from models.product import ProductModel


data = [
    {
        "model": UserModel,
        "data": [
            {"username": "admin", "password": "123", "role": "admin", "active": True},
            {"username": "hari", "password": "123", "role": "user", "active": True},
            {"username": "manu", "password": "123", "role": "user", "active": True},
            {"username": "sebin", "password": "123", "role": "user", "active": False},
        ],
    },
    {
        "model": CategoryModel,
        "data": [
            {"name": "toys"},
            {"name": "food"},
            {"name": "electronics"},
        ],
    },
    {
        "model": ProductModel,
        "data": [
            {"name": "remote car", "price": 10, "category_id": 1},
            {"name": "ball", "price": 10, "category_id": 1},
            {"name": "bat", "price": 10, "category_id": 1},
            {"name": "biriyani", "price": 10, "category_id": 2},
            {"name": "neychor", "price": 10, "category_id": 2},
            {"name": "camera", "price": 10, "category_id": 3},
            {"name": "speker", "price": 10, "category_id": 3},
        ],
    },
]


print("data generation started")
with app.app_context():
    db.drop_all()
    print("all tables dropped")
    db.create_all()
    print("all tables created again")
    for item in data:
        print(f'generating data for {str(item["model"].__qualname__)}', end="")
        count = 0
        for row in item["data"]:
            entry = item["model"](**row)
            entry.save()
            count += 1
        print(f" - entries completed {count}")
print("data generation completed")
