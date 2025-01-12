from db import db
from models.base import BaseModel


class CategoryModel(BaseModel):
    name = db.Column(db.String(20), nullable=False, unique=True)

    def json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
        }
