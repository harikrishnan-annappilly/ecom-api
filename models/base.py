from db import db
from typing import TypeVar, Type
from sqlalchemy.orm import Mapped

T = TypeVar("T", bound="BaseModel")


class BaseModel(db.Model):
    __abstract__ = True
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)

    def json(self) -> dict:
        return {"class": "base class"}

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def _find(cls, **kwargs):
        condition = [
            getattr(cls, key) == value if not key.startswith("not_") else getattr(cls, key.replace("not_", "")) != value
            for key, value in kwargs.items()
        ]
        return cls.query.filter(*condition)

    @classmethod
    def find_one(cls: Type["T"], **kwargs) -> Type["T"]:
        return cls._find(**kwargs).first()

    @classmethod
    def find_all(cls: Type["T"], **kwargs) -> list[T]:
        return cls._find(**kwargs).all()
