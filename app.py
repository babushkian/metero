import os
import json
import time
from pprint import pprint
import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, flash, session, g, current_app
from flask import jsonify, Response

from flask_cors import cross_origin
from flask_login import login_required, login_user, current_user, logout_user
from wtforms import Label
from sqlalchemy import func, exists, distinct, and_


from model import db, login_manager
from model.tables import Meters, Users, Measures, Dates

from forms import LoginForm, RegisterForm, MeasurementsForm, MeasurementInpit
from cred import Cred

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{Cred.my_user}:{Cred.my_pass}@localhost/meteror'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
#app.config['SECRET_KEY'] = 'asonaeusebowerkwdeevkueauweytvuroasgv'
app.config['FLASK_DEBUG'] = False

db.init_app(app)

login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Для внесения показаний нужно авторизоваться.'
login_manager.login_message_category = 'danger'



@app.route("/")
def index():
    # print(session)
    # print(current_app)
    # print('type:', type(current_app))
    # print('property:', dir(current_app))
    header = "На этом сайте можно легко и просто вести учет показаний домашних счетчкиков. Воды, тепла, электричества... да чего угодно! Даже веса своей тещи."
    content = ["Это учебный проект, который представляет собой приложение для учета показаний счетчиков.",
               "Здесь можно зарегистрироваться, завести неколько счетчиков, отсортировать их в удобном порядке и вносить показания.",
               " Если что-то введено неправильно, записи можно исправлять.",
               "Для ознакомления с функционалом сайта я сделал несколько учетных записей:",
               "dimba@mail.ru", "kos@mail.ru", "f@f.ru", "vas@mail.ru", "Пароли у всех аккаунтов: «1234».", "Меня зовут Дима, будем знакомы))). Мне можно написать в телегу <b>@sakalof</b>."]
    return render_template("index.html",
                           title="Главная",
                           comment=header, content=content)


@app.route("/edit_measurement/",  methods=("POST",))
@login_required
def edit_measurement():

    form = MeasurementsForm()
    # берем дату для заполнения первого поля: дата
    did = int(request.form["subbutton"])
    if did != 0:
        q = db.select(Dates).where(Dates.id == did)
        date_edit = db.session.execute(q).scalar_one_or_none()
        if date_edit is None:
            flash("Отсутствует указанная дата", category='danger')
            return redirect(url_for('meters_table'))
        form.date.data = date_edit.date
        form.date_id.data = date_edit.id
        date_id = date_edit.id
    else:
        date_id = did

    # пронумерованный список имен счетчиков
    q = db.select(func.row_number().over(order_by='order').label('number'), Meters.name, Meters.id).where(
        Meters.user_id == current_user.id).order_by(Meters.order)
    meter_ids = db.session.execute(q).all()

    ent = list()
    measurements = Measures.with_date_id(date_id)

    # делаем словарь, где id счетчика сопоставлены данные измерения
    exist_measurements = {}
    for r in measurements:
        exist_measurements[r.meter_id] = r.data
    for rec in meter_ids:
        e = MeasurementInpit()
        ee = e.entry
        entry_id = f'{e.ENTRY_TITLE}{rec.number}'
        ee.id = entry_id
        ee.name = entry_id
        ee.data = exist_measurements.get(rec.id)
        ee.label = Label(field_id=entry_id, text=rec.name)
        ent.append(e)
    form.entries = ent
    form.submit.label.text = "Изменить" if did else "Внести"
    comment_string = f"{'Изменение' if did else 'Внесение'} показаний"
    return render_template("measurement.html", title=comment_string, comment=comment_string,
                           form=form)


@app.route("/edit_measurement_data", methods=("POST",))
@login_required
def edit_measurement_data():
    q = db.select(func.row_number().over(order_by='order').label('number'), Meters).where(
        Meters.user_id == current_user.id).order_by(Meters.order)
    meter_ids = db.session.execute(q).all()
    # словарь, где в ключах содержатся номера счетчиков (для удобства), а в значениях id-шники счетчиков в таблице
    meters_dict = {rec.number: rec.Meters.id for rec in meter_ids}

    conv_date = datetime.datetime.strptime(request.form["date"], "%Y-%m-%d").date()
    # если дата существует, возвращается ее id, иначе дата создается и возвращается id
    date_id = Dates.get_edited_date_id(conv_date)

    origin_date_id = int(request.form["date_id"])
    action = "изменена" if origin_date_id else "добавлена"
    # признак новой записи - дата в форму не передавалась


    # проверяем, нет ли уже показаний за эту дату, внесенных данным пользователем, если да, то ошибка
    # если в ходе редактирования дата не изменялась, можно не проверять
    if origin_date_id != date_id and Measures.with_date_id(date_id):
        flash("Ошибка! Запись с такой датой уже существует.", category='danger')
        return redirect(url_for('meters_table'))
    # запись новая, дата не менялась, аоэтому нужно откудато получать старые версии данных
    # получаем из записей за ту же дату
    if origin_date_id == 0:
        origin_date_id = date_id

    # Изменение записей происходит таким образом: идет выборка за старую дату, получается запись,
    # и ей присваиваются новая дата и/или новые данные
    # если старой даты нет, выборку откуда-то производить надо
    for i in request.form:
        # добавляем показания в базу (обрабатываем динамические поля с названиями счетчиков)
        if i.startswith(MeasurementInpit.ENTRY_TITLE):
            form_entry_id = int(i.removeprefix(MeasurementInpit.ENTRY_TITLE))
            meter_id = meters_dict[form_entry_id]
            # в цикле ищем запись для конкретного счетчика за конкретное число для текущего пользователя
            measurement = Measures.specific_record(origin_date_id, meter_id)
            # переписываем даты для всех записей, независимо от того, менялась дата или нет (чтобы не городить лишние усооваия)
            if measurement:
                if measurement.data != request.form[i] or measurement.date_id != date_id:
                    measurement.date_id = date_id
                    measurement.data = request.form[i]
            else:
                m = Measures(meter_id=meter_id, user_id=current_user.id, date_id=date_id, data=request.form[i])
                db.session.add(m)
    db.session.commit()
    flash(f"Запись {action}", category='success')
    return redirect(url_for('meters_table'))


@app.route("/example/",  methods=("POST",))
@login_required
def example():
    print("свойства формы:")
    for i in request.form:
        print(request.form[i])
    return render_template("example.html", form = request.form)


@app.route("/del_measurement_post/",  methods=("POST",))
@login_required
def del_measurement_post():

    date_id = int(request.form["subbutton"])

    q = (db.delete(Measures)
         .where(Measures.user_id == current_user.id)
         .where(Measures.date_id == date_id)
         )
    measurements = db.session.execute(q)
    db.session.commit()

    return redirect(url_for('meters_table'))




@app.route("/meters_table", methods=("POST", "GET"))
def meters_table():
    table_dict = return_table_data(current_user.id)
    return render_template('meters_table.html',
                           title='Показания счетчиков',
                           comment='Показания счетчиков',
                           table_dict=table_dict)


def return_table_data(user_id):
    a = (db.select(Measures, Dates.date.label('date_name'), Meters.name.label('meter_name'), Meters.order.label('order'))
         .filter(Measures.user_id == user_id)
         .join(Dates, Dates.id == Measures.date_id)
         .join(Meters, Meters.id == Measures.meter_id)
         ).subquery()
    # сипсок неповторяющихся дат
    t_time = db.select(distinct(a.c.date_id), a.c.date_name).order_by(a.c.date_name.desc())
    table_date = db.session.execute(t_time).all()
    date_dict = {t[0]: t[1] for t in table_date}

    # список счетчиков
    # t_meters = db.select(distinct(a.c.meter_id), a.c.meter_name).order_by(a.c.order)
    t_meters = db.select(distinct(a.c.meter_id),a.c.meter_name, a.c.order).order_by(a.c.order)
    table_head = db.session.execute(t_meters).all()

    # показания счетчиков: id счетчика, id даты, показания
    t_data = db.select(a.c.meter_id, a.c.date_id, a.c.data).order_by(a.c.order)
    table_data = db.session.execute(t_data).all()
    # data_dict:{date_id: {meter_id: measurement, }, }
    data_dict: dict[int, dict[int, float]] = {}
    for rec in table_data:
        meter_index = rec[0]
        time_index = rec[1]
        data = rec[2]
        if not data_dict.get(time_index):
            data_dict[time_index] = {}
        data_dict[time_index][meter_index] = data

    table_list = []
    for date_id in date_dict:
        line = [date_dict[date_id].strftime('%d.%m.%Y')]

        for m in table_head:
            dd = data_dict[date_id].get(m[0])
            line.append(dd if dd is not None else "-")
        table_list.append({"id": date_id, "data": line})

    head = [i[1] for i in table_head]
    head = ['дата'] + head

    jsonlike = {'head': head, "measurements": table_list}
    return jsonlike



@app.route("/register", methods=("POST", "GET"))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        is_duplicated = db.session.execute(db.select(Users).filter(Users.email == form.email.data)).one_or_none()
        if is_duplicated:
            flash('Пользователь с таким почтовым адресом уже существует', category='danger')
            return redirect(url_for('register'))
        try:
            hash = generate_password_hash(form.password1.data)
            u = Users(name=form.name.data, email=form.email.data, psw=hash)
            db.session.add(u)
            db.session.commit()
            flash('Вы успешно зарегистрированы', category='success')
            return redirect(url_for('login'))
        except:
            flash('Что-то пошло не так.', category='danger')

    return render_template("register.html", title="Регистрация",
                           comment="Зарегистрируйтесь, пожалуйста", form=form)


@app.route("/login", methods=("POST", "GET"))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        uq = db.select(Users).filter(Users.email == form.email.data)
        user = db.session.execute(uq).scalar_one_or_none()

        if user:
            if check_password_hash(user.psw, form.password.data):
                rem = form.remember_me.data
                login_user(user, remember=rem)
                return redirect(request.args.get('next') or url_for('dashboard'))
            else:
                flash('Неверный пароль', category='danger')
        else:
            flash('Пользователь не существует', category='danger')
    # form = LoginForm()
    return render_template("login.html", title="Вход", comment="Авторизация", form=form)

@app.route("/logout", methods=("POST", "GET"))
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/dashboard", methods=("POST", "GET"))
@login_required
def dashboard():
    u = db.get_or_404(Users, current_user.id)
    msg = f'Добро пожаловать, {u.name} ({u.email})'
    return render_template("dashboard.html",
                           title="Личный кабинет",
                           comment=msg,
                           user=u)


@app.route("/api/get_meters/", methods=["GET"])
@cross_origin()
@login_required
def get_meters():
    tblq = db.select(Meters).filter(Meters.user_id == current_user.id)
    tbl = db.session.execute(tblq).scalars().all()
    meter_list = []
    for i in tbl:
        meter_list.append(i.as_dict())
    response = jsonify(meter_list)
    return response


@app.route("/api/add_rec/", methods=["POST"])
@cross_origin()
@login_required
def api_add_rec():
    j = request.json
    q = db.select(func.max(Meters.order)).where(Meters.user_id == j["user_id"])
    max_ord = db.session.execute(q).scalar()

    max_ord = max_ord if max_ord else 0
    j["order"] = max_ord + 1
    m = Meters(**j)
    db.session.add(m)
    db.session.commit()
    return "text"

@app.route("/api/del_rec/", methods=["POST"])
@cross_origin()
@login_required
def api_del_rec():
    rid = request.json["id"]
    # d = db.delete(Measures).where(Measures.meter_id == rid)
    # db.session.execute(d)
    meter_rec = Meters.with_id(rid)
    db.session.delete(meter_rec)
    db.session.commit()
    resp = Response('', 200)
    return resp

@app.route("/api/swap/", methods=["POST"])
@cross_origin()
@login_required
def api_swap():
    ids = request.json
    r1 = Meters.with_id(ids["from"])
    r2 = Meters.with_id(ids["to"])
    r1.order, r2.order = r2.order, r1.order
    db.session.commit()
    resp = Response('', 200)
    return resp


@app.route("/api/nameedit/", methods=["POST"])
@cross_origin()
def api_nameedit():
    """
    изменение имени счетчика
    """
    meter_dict = request.json
    meter_rec = Meters.with_id(meter_dict["id"])
    meter_rec.name = meter_dict["name"]
    db.session.commit()

    resp = Response('', 200)
    return resp



if __name__ == "__main__":
    app.run()
