from sqlalchemy import String, Float, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class PriceRecord(Base):
    __tablename__ = "price_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    ticker: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)

