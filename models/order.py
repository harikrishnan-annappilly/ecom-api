from db import db
from models.base import BaseModel
from sqlalchemy.orm import Mapped
from datetime import datetime
import pytz

ist = pytz.timezone("Asia/Kolkata")


class OrderMainModel(BaseModel):
    user_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey("user_model.id"), nullable=False)
    date: Mapped[datetime] = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(ist))
    grand_total: Mapped[float] = db.Column(db.Float, nullable=False, default=0)
    address: Mapped[str] = db.Column(db.String, nullable=False)

    order_subs: Mapped[list["OrderSubModel"]] = db.relationship("OrderSubModel", backref="order_main", lazy=True)

    def json(self):
        order_sub = [{"name": order_sub.product.name} for order_sub in self.order_subs]
        return {
            "user_id": self.user_id,
            "date": str(self.date),
            "grand_total": self.grand_total,
            "order_sub": order_sub,
        }

    def full_json(self):
        return {
            "user_id": self.user_id,
            "date": str(self.date),
            "grand_total": self.grand_total,
            "order_sub": [order_sub.json() for order_sub in self.order_subs],
        }


class OrderSubModel(BaseModel):
    order_main_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey("order_main_model.id"), nullable=False)
    product_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey("product_model.id"), nullable=False)
    qty: Mapped[int] = db.Column(db.Integer, nullable=False)
    price: Mapped[float] = db.Column(db.Float, nullable=False)
    total: Mapped[float] = db.Column(db.Float, nullable=False)

    def json(self):
        return {
            "product": self.product.json(),
            "price": self.price,
            "qty": self.qty,
            "total": self.total,
        }
