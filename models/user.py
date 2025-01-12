from db import db
from models.base import BaseModel


class UserModel(BaseModel):
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")
    active = db.Column(db.Boolean, default=True)

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "role": self.role,
            "active": self.active,
        }
