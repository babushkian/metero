import os


from flask import Flask

from model import db
from model.tables import Meters, Users, Measures, Dates, Actions
from data_for_base import *
from cred import Cred

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{Cred.my_user}:{Cred.my_pass}@localhost/meteror'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


db.init_app(app)

print("метадата:")
print(dir(db.metadata))
print(db.metadata.tables)
print(db.metadata.info)
print(db.metadata.schema)



def get_variable_name(table):
    print("=================================")
    tn = table.__table__.name
    print('имя таблицы: ', tn)
    for name in globals():
        print(name)
        if name == tn:
            return globals()[name]
    return None


def populate_table(table):
    lst = get_variable_name(table)
    print(lst)
    print("="*40)
    print("=" * 40)
    for rec in lst:
        print(rec)
        ex = table(**rec)
        db.session.add(ex)
        db.session.commit()


with app.app_context():
    db.drop_all()
    db.create_all()
    for t in [Dates, Users, Meters, Measures, Actions]:
        populate_table(t)

