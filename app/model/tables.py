from __future__ import annotations
import datetime
from typing import Any
from flask_login import UserMixin, current_user
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Date, DateTime
from app.model import  Base


class Users(Base, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    psw: Mapped[str] = mapped_column(String(500))
    date: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now
    )
    meters: Mapped[list[Meters]] = relationship("Meters", back_populates="user")
    measures: Mapped[list[Measures]] = relationship("Measures", back_populates="user")

    def __repr__(self):
        return f"<Users (id={self.id},  name={self.name}, email={self.email})>"


class Dates(Base):
    __tablename__ = "dates"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date, unique=True)
    measures: Mapped[list[Measures]] = relationship("Measures", back_populates="date")

    def __repr__(self) -> str:
        return f"<Dates (id={self.id},  date={self.date})>"


class Meters(Base):
    __tablename__ = "meters"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    order: Mapped[int]
    user: Mapped[Users] = relationship("Users", back_populates="meters")
    measures: Mapped[list[Measures]] = relationship(
        "Measures", back_populates="meter"
    )

    def __repr__(self) -> str:
        return f"<Mertes (id={self.id},  name={self.name}, user_id={self.user_id})>"

    def as_dict(self) -> dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Measures(Base):
    __tablename__ = "measures"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE")
    )
    meter_id: Mapped[int] = mapped_column(ForeignKey("meters.id", ondelete="CASCADE"))
    date_id: Mapped[int] = mapped_column(ForeignKey("dates.id", ondelete="CASCADE")
    )
    data: Mapped[float]
    user: Mapped[Users] = relationship("Users", back_populates="measures")
    meter: Mapped[Meters] = relationship("Meters", back_populates="measures")
    date: Mapped[Dates] = relationship("Dates", back_populates="measures")

    def __repr__(self):
        return f"<Measure (id={self.id},  user={self.user_id}, date={self.date_id}, data={self.data})>"

