from db import db
from models.base import BaseModel


class CartModel(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey("user_model.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product_model.id"), nullable=False)
    qty = db.Column(db.Integer, nullable=False, default=1)

    def json(self):
        return {
            "id": self.id,
            "product": {"id": self.product_id, "name": self.product.name},
            "qty": self.qty,
        }

    def __str__(self):
        return self.json()
