import datetime
from flask_login import UserMixin, current_user
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Column, Integer, String, Date
from app.model import login_manager, db


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True)
    psw = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f"<Users (id={self.id},  name={self.name}, email={self.email})>"


class Dates(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date = mapped_column(Date, unique=True, nullable=False)

    def __repr__(self):
        return f"<Dates (id={self.id},  date={self.date})>"

    @staticmethod
    def date_id_exists(date_id: int) -> bool:
        date_id_query = db.select(Dates).where(Dates.id == date_id)
        res = db.session.execute(date_id_query).scalar_one_or_none()
        return res is not None

    @staticmethod
    def date_exists(date: datetime.date):
        date_query = db.select(Dates).where(Dates.date == date)
        date_obj = db.session.execute(date_query).scalar_one_or_none()
        return date_obj

    @staticmethod
    def get_edited_date_id(conv_date: datetime.date) -> int:
        date_id = Dates.date_exists(conv_date)
        if date_id is None:
            date_id = Dates(date=conv_date)
            db.session.add(date_id)
            db.session.commit()
        return date_id.id


class Meters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    order = db.Column(db.Integer)

    def __repr__(self):
        return f"<Mertes (id={self.id},  name={self.name}, user_id={self.user_id})>"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @staticmethod
    def with_id(id_):
        print(id_, type(id_))
        q = db.select(Meters).where(Meters.id == id_)
        return db.session.execute(q).scalar()

    @staticmethod
    def with_current_user():
        q = db.select(Meters).filter(Meters.user_id == current_user.id)
        return db.session.execute(q).scalars().all()


class Measures(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    meter_id = db.Column(db.Integer, db.ForeignKey("meters.id", ondelete="CASCADE"))
    date_id = db.Column(db.Integer, db.ForeignKey("dates.id", ondelete="CASCADE"))
    data = db.Column(db.Float)

    def __repr__(self):
        return f"<Measure (id={self.id},  user={self.user_id}, date={self.date_id}, data={self.data})>"

    @staticmethod
    def with_date_id(date_id: int):
        q = (
            db.select(Measures)
            .where(Measures.user_id == current_user.id)
            .where(Measures.date_id == date_id)
        )
        msmnts = db.session.execute(q).scalars().all()
        return msmnts

    @staticmethod
    def specific_record(date, meter):
        q = (
            db.select(Measures)
            .where(Measures.user_id == current_user.id)
            .where(Measures.date_id == date)
            .where(Measures.meter_id == meter)
        )
        measurement = db.session.execute(q).scalar_one_or_none()
        return measurement


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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
