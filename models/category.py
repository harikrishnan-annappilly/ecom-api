from db import db
from models.base import BaseModel, T
from sqlalchemy.orm import Mapped


class CategoryModel(BaseModel):
    name: Mapped[str] = db.Column(db.String(20), nullable=False, unique=True)
    products: Mapped[list["T"]] = db.relationship(
        "ProductModel", backref="category", lazy=True, cascade="all, delete-orphan"
    )

    def json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
        }
