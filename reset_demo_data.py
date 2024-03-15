import os
from flask import Flask
from model import db
from model.tables import Meters, Users, Measures, Dates, Actions
from data_for_base import *
from cred import Cred


class User:
    def __init__(self, rec):
        self.date = rec['date']
        self.email = rec['email']
        self.name = rec['name']
        self.psw = rec['psw']
        self.meters = []

    def __repr__(self):
        s = f'User {self.name}  {self.email}  {self.date}\n'
        for m in self.meters:
            s += repr(m)
        return s

    def populate(self):
        db.session.add(Users(date=self.date, email=self.email, name=self.name, psw=self.psw))
        db.session.commit()
        q = db.select(Users.id).where(Users.name == self.name)
        uid = db.session.execute(q).scalar()
        for m in self.meters:
            m.populate(uid)


class Meter:
    def __init__(self, rec):
        self.id = None
        self.name = rec["name"]
        self.order = rec["order"]
        self.measures = []

    def __repr__(self):
        s = f'\tMeter {self.name}\n'
        for i in self.measures:
            s += repr(i)
        return s

    def populate(self, user_id):
        db.session.add(Meters(name=self.name, user_id=user_id, order=self.order))
        db.session.commit()
        q = db.select(Meters.id).where(Meters.name == self.name).where(Meters.user_id == user_id)
        mid = db.session.execute(q).scalar()
        for m in self.measures:
            db.session.add(Measures(user_id=user_id, meter_id=mid, date_id=m.date_id, data=m.data))
        db.session.commit()


class Measure:
    def __init__(self, rec):
        self.date_id = rec["date_id"]
        self.data = rec["data"]

    def __repr__(self):
        return f'\t\tMeasure {self.data}\n'

new_users = {}
for dc in users:
    user_id = dc['id']
    new_users[user_id] = User(dc)

new_meters = {}
for m in meters:
    meter_id = m["id"]
    user_id = m["user_id"]
    new_meters[meter_id] = Meter(m)
    new_users[user_id].meters.append(new_meters[meter_id])


for m in measures:
    meter_id = m["meter_id"]
    new_meters[meter_id].measures.append(Measure(m))



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{Cred.my_user}:{Cred.my_pass}@{Cred.host}/{Cred.base}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


db.init_app(app)
with app.app_context():
    for u in new_users.values():
        q = db.delete(Users).where(Users.name == u.name)
        measurements = db.session.execute(q)
    db.session.commit()

    for u in new_users.values():
        u.populate()

