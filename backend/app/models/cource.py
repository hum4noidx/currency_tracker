from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Cource(Base):
    __tablename__ = "cource"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    trade_pair: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    exchange_id: Mapped[int] = mapped_column(ForeignKey("exchanger.id"), nullable=False)

    exchanger = relationship("Exchanger", back_populates="courses")
