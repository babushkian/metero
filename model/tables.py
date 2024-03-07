from datetime import datetime
from flask_login import UserMixin, current_user

from model import login_manager
from model import db


class Users(db.Model,  UserMixin ):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Users (id={self.id},  name={self.name}, email={self.email})>"

class Dates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False)

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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    meter_id = db.Column(db.Integer, db.ForeignKey('meters.id', ondelete='CASCADE'))
    date_id = db.Column(db.Integer, db.ForeignKey('dates.id', ondelete='CASCADE'))
    data = db.Column(db.Float)

    def __repr__(self):
        return f"<Measure (id={self.id},  user={self.user_id}, date={self.date_id}, data={self.data})>"

    @staticmethod
    def with_date_id(date_id: int):
        q = (db.select(Measures)
             .where(Measures.user_id == current_user.id)
             .where(Measures.date_id == date_id)
             )
        msmnts = db.session.execute(q).scalars().all()
        return msmnts

    @staticmethod
    def specific_record(date, meter):
        q = (db.select(Measures)
             .where(Measures.user_id == current_user.id)
             .where(Measures.date_id == date)
             .where(Measures.meter_id == meter)
             )
        measurement = db.session.execute(q).scalar_one_or_none()
        return measurement

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)



