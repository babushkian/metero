# from __future__ import annotations
import datetime
from typing import Any
from flask_login import UserMixin, current_user
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, Date, DateTime, select
from app.model import login_manager, db


class Users(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    psw: Mapped[str] = mapped_column(String(500))
    date: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now
    )
    meters: Mapped[list["Meters"]] = relationship("Meters", back_populates="user")
    measures: Mapped[list["Measures"]] = relationship("Measures", back_populates="user")

    def __repr__(self):
        return f"<Users (id={self.id},  name={self.name}, email={self.email})>"


class Dates(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date, unique=True)
    measures: Mapped[list["Measures"]] = relationship("Measures", back_populates="date")

    def __repr__(self) -> str:
        return f"<Dates (id={self.id},  date={self.date})>"


class Meters(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    order: Mapped[int]
    user: Mapped[Users] = relationship("Users", back_populates="meters")
    measures: Mapped[list["Measures"]] = relationship(
        "Measures", back_populates="meter"
    )

    def __repr__(self) -> str:
        return f"<Mertes (id={self.id},  name={self.name}, user_id={self.user_id})>"

    def as_dict(self) -> dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Measures(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE")
    )
    meter_id: Mapped[int] = mapped_column(ForeignKey("meters.id", ondelete="CASCADE"))
    date_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("dates.id", ondelete="CASCADE")
    )
    data: Mapped[float]
    user: Mapped[Users] = relationship("Users", back_populates="measures")
    meter: Mapped[Meters] = relationship("Meters", back_populates="measures")
    date: Mapped[Dates] = relationship("Dates", back_populates="measures")

    def __repr__(self):
        return f"<Measure (id={self.id},  user={self.user_id}, date={self.date_id}, data={self.data})>"


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


class UsrLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    action = db.Column(db.Integer, db.ForeignKey("actions.id"))
    info = db.Column(db.String(255))
    date = db.Column(
        db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    ip = db.Column(db.String(16))

    def __repr__(self):
        return f"<Log (id={self.id},  user_id={self.user_id}, date={self.date}, action={self.action})>"

    @staticmethod
    def login_attempt(username, ip):
        db.session.add(UsrLog(action=11, info=username, ip=ip))
        db.session.commit()

    @staticmethod
    def login(ip):
        db.session.add(UsrLog(user_id=current_user.id, action=2, ip=ip))
        db.session.commit()

    @staticmethod
    def logout(ip):
        rec = UsrLog(user_id=current_user.id, action=3, ip=ip)
        print(rec)
        db.session.add(rec)
        db.session.commit()

    @staticmethod
    def add_meter(ip, name):
        q = (
            db.select(Meters.id)
            .where(Meters.user_id == current_user.id)
            .where(Meters.name == name)
        )
        meter_id = db.session.execute(q).scalar()
        info = f"{meter_id}, {name}"
        db.session.add(UsrLog(user_id=current_user.id, action=4, info=info, ip=ip))
        db.session.commit()

    @staticmethod
    def rename_meter(ip, meter_id, name):
        info = f"{meter_id}, {name}"
        db.session.add(UsrLog(user_id=current_user.id, action=5, info=info, ip=ip))

    @staticmethod
    def delete_meter(ip, meter_id):
        db.session.add(
            UsrLog(user_id=current_user.id, action=6, info=str(meter_id), ip=ip)
        )

    @staticmethod
    def edit_measures(ip, ed_date, is_old):
        db.session.add(
            UsrLog(
                user_id=current_user.id, action=(7 + is_old), info=str(ed_date), ip=ip
            )
        )
        db.session.commit()

    @staticmethod
    def delete_measures(
        ip,
        date_id,
    ):
        q = db.select(Dates.date).where(Dates.id == date_id)
        ed_date = db.session.execute(q).scalar_one_or_none()
        db.session.add(
            UsrLog(user_id=current_user.id, action=9, info=str(ed_date), ip=ip)
        )
        db.session.commit()


class Actions(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
