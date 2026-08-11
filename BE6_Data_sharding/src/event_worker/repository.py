from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.product import Product


class ProductReadRepository:
    """Worker uchun mahsulotlarni faqat o‘qiydigan repository."""

    def __init__(self, db: Session):
        self.db = db

    def get_random(self) -> Product | None:
        statement = (
            select(Product)
            .order_by(func.random())
            .limit(1)
        )

        return self.db.scalar(statement)
