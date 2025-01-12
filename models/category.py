from db import db
from models.base import BaseModel
from sqlalchemy.orm import Mapped


class CategoryModel(BaseModel):
    name: Mapped[str] = db.Column(db.String(20), nullable=False, unique=True)

    def json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
        }
