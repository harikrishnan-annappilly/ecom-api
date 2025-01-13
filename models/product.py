from db import db
from sqlalchemy.orm import Mapped
from models.base import BaseModel


class ProductModel(BaseModel):
    name: Mapped[str] = db.Column(db.String(20), nullable=False, unique=True)
    price: Mapped[float] = db.Column(db.Float, nullable=False, default=1)
    category_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey("category_model.id"))

    def json(self):
        self.category: BaseModel
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "category": self.category.json() if self.category else {"id": "#na", "name": "#na"},
        }
