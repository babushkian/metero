import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, redirect, url_for, flash
from flask import jsonify, Response, Blueprint

from flask_cors import cross_origin
from flask_login import login_required

from sqlalchemy import func, exists, distinct, and_
from app.repositories.date_repository import DateRepository
from app.repositories.meter_repository import MetersRepository
from app.repositories.measure_repository import MeasureRepository

from app.model import db
from app.model.tables import Meters, UsrLog


bp = Blueprint("api", __name__, url_prefix="/api")

print(bp)


@bp.route("/get_meters/", methods=["GET"])
@cross_origin()
@login_required
def get_meters():
    mr = MetersRepository()
    tbl = mr.with_current_user()
    meter_list = []
    for i in tbl:
        meter_list.append(i.as_dict())
    response = jsonify(meter_list)
    return response


@bp.route("/add_rec/", methods=["POST"])
@cross_origin()
@login_required
def api_add_rec():
    j = request.json
    j["name"] = j["name"][:45]
    q = db.select(func.max(Meters.order)).where(Meters.user_id == j["user_id"])
    max_ord = db.session.execute(q).scalar()

    max_ord = max_ord if max_ord else 0
    j["order"] = max_ord + 1
    m = Meters(**j)
    db.session.add(m)
    db.session.commit()
    UsrLog.add_meter(request.remote_addr, j["name"])
    return Response("", 200)


@bp.route("/del_rec/", methods=["POST"])
@cross_origin()
@login_required
def api_del_rec():
    rid = request.json["id"]
    mr = MetersRepository()
    meter_rec = mr.with_id(rid)
    db.session.delete(meter_rec)
    UsrLog.delete_meter(request.remote_addr, rid)
    db.session.commit()
    resp = Response("", 200)
    return resp


@bp.route("/swap/", methods=["POST"])
@cross_origin()
@login_required
def api_swap():
    # изначально делал обмен ментами в рамках транзакции, но с @login_required это не работает
    # говорит, что транзакция уже началась
    mr = MetersRepository()
    cu_meters = mr.with_current_user()
    ids = request.json
    r1 = mr.with_id(ids["from"])
    r2 = mr.with_id(ids["to"])
    # прежде чем менять местами счетчики, надо убедиться, что они принадлежат текущему юзеру (для безопасности)
    if r1 in cu_meters and r2 in cu_meters:
        r1.order, r2.order = r2.order, r1.order
        db.session.commit()
    resp = Response("", 200)
    return resp


@bp.route("/nameedit/", methods=["POST"])
@cross_origin()
@login_required
def api_nameedit():
    """
    изменение имени счетчика
    """
    meter_dict = request.json
    mr = MetersRepository()
    meter_rec = mr.with_id(meter_dict["id"])
    meter_rec.name = meter_dict["name"][:45]
    UsrLog.rename_meter(request.remote_addr, meter_rec.id, meter_rec.name)
    db.session.commit()

    resp = Response("", 200)
    return resp
