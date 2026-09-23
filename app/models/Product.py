from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(index=True)
    price: Mapped[int]
    desc: Mapped[str]
    is_offer: Mapped[bool]

    embedding: Mapped[list[float]] = mapped_column(Vector(3072), nullable=True)