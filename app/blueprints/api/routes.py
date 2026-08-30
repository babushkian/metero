import datetime

from flask import (
    Blueprint,
    Response,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_cors import cross_origin
from flask_login import login_required
from sqlalchemy import and_, distinct, exists, func
from werkzeug.security import check_password_hash, generate_password_hash
from app.model import   SessionLocal
from app.model import db
from app.model.tables import Meters
from app.repositories.date_repository import DateRepository
from app.repositories.measure_repository import MeasureRepository
from app.repositories.meter_repository import MetersRepository

bp = Blueprint("api", __name__, url_prefix="/api")



@bp.route("/get_meters/", methods=["GET"])
@cross_origin()
@login_required
def get_meters():
    with SessionLocal() as session:
        mr = MetersRepository(session)
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
    user_id =j["user_id"]
    with SessionLocal() as session:
        mr = MetersRepository(session)
        max_ord = mr.get_max_order(user_id)

        max_ord = max_ord if max_ord else 0
        j["order"] = max_ord + 1
        m = Meters(**j)
        session.add(m)
        session.commit()
    return Response("", 200)


@bp.route("/del_rec/", methods=["POST"])
@cross_origin()
@login_required
def api_del_rec():
    rid = request.json["id"]
    with SessionLocal() as session:
        mr = MetersRepository(session)
        meter_rec = mr.with_id(rid)
        session.delete(meter_rec)
        session.commit()
    resp = Response("", 200)
    return resp


@bp.route("/swap/", methods=["POST"])
@cross_origin()
@login_required
def api_swap():
    # изначально делал обмен ментами в рамках транзакции, но с @login_required это не работает
    # говорит, что транзакция уже началась
    ids = request.json
    with SessionLocal() as session:
        mr = MetersRepository(session)
        cu_meters = mr.with_current_user()
    
        r1 = mr.with_id(ids["from"])
        r2 = mr.with_id(ids["to"])
        # прежде чем менять местами счетчики, надо убедиться, что они принадлежат текущему юзеру (для безопасности)
        if r1 in cu_meters and r2 in cu_meters:
            r1.order, r2.order = r2.order, r1.order
        session.commit()
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
    with SessionLocal() as session:
        mr = MetersRepository(session)
        meter_rec = mr.with_id(meter_dict["id"])
        meter_rec.name = meter_dict["name"][:45]
        session.commit()

    resp = Response("", 200)
    return resp
