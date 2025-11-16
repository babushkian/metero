import os
import sys
from pprint import pprint





from data_for_base import *
from dotenv import load_dotenv


# Определяем путь до корня проекта (один уровень выше текущего файла)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from app import create_app, db
from model.tables import Meters, Users, Measures, Dates, Actions
load_dotenv()

# Получаем URL из переменной окружения
DATABASE_URL = os.getenv("DATABASE_URL")



print("метадата:")
print(dir(db.metadata))
print("*****************************************")
for table in db.metadata.tables:
    pprint(table)
    pprint(db.metadata.tables[table])
print("*****************************************")
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


app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
    for t in [Dates, Users, Meters, Measures, Actions]:
        populate_table(t)

