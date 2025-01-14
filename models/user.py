from db import db
from models.base import BaseModel
from sqlalchemy.orm import Mapped


class UserModel(BaseModel):
    username: Mapped[str] = db.Column(db.String(20), nullable=False, unique=True)
    password: Mapped[str] = db.Column(db.String(20), nullable=False)
    role: Mapped[str] = db.Column(db.String(20), nullable=False, default="user")
    active: Mapped[bool] = db.Column(db.Boolean, default=True)

    carts = db.relationship("CartModel", backref="user", lazy=True, cascade="all, delete-orphan")

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "role": self.role,
            "active": self.active,
        }
