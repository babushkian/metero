


from pprint import pprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from sqlalchemy.sql import select
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, Float

from model import db
from model.tables import Meters, Users, Measures, Dates

engine = create_engine(f"sqlite:///instance/blog.db", echo=False)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


py_file = open('data_for_base.py', 'w', encoding='utf-8')
py_file.write("from datetime import date, datetime\n")


def proc_bool(d):
    return d


def proc_int(d):
    return d


def proc_str(d):
    return f'"{d}"'


def proc_date(d):
    return f"date({d.year}, {d.month}, {d.day})"


def proc_datetime(d):
    return f"datetime({d.year}, {d.month}, {d.day}, {d.hour}, {d.minute}, {d.second})"

type_process = {Integer: proc_int, Float: proc_int, String: proc_str, Date: proc_date, DateTime:proc_datetime}
def create_py_from_sql(table):

    col_names = {n.name: n.type  for n in table.__table__.columns}
    print(col_names)
    pc = select(table)
    res = session.execute(pc).scalars()
    data = []
    for i in res:
        row = {}
        for name in col_names:
            row[name] =  type_process[type(col_names[name])](getattr(i, name))
        dr  = [f'"{r}":{row[r]}' for r in row]
        rec_str = f"{{{', '.join(dr)}}}"
        data.append(rec_str)
    table_content = ""
    for d in data:
        table_content += f"\t{d},\n"
    s = f"{table.__table__.name} = [\n{table_content}]"
    return s+ '\n'


for ta in [Meters, Users, Measures, Dates]:

    x = create_py_from_sql(ta)
    py_file.write(x)
