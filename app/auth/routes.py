from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, redirect, url_for, flash
from flask import Blueprint

from flask_login import login_required, login_user, current_user, logout_user

from app.model import db, login_manager
from app.model.tables import Users, UsrLog

from app.main.forms import LoginForm, RegisterForm

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("POST", "GET"))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        is_duplicated = db.session.execute(
            db.select(Users).filter(Users.email == form.email.data)
        ).one_or_none()
        if is_duplicated:
            flash(
                "Пользователь с таким почтовым адресом уже существует",
                category="danger",
            )
            return redirect(url_for("auth.register"))
        try:
            hash = generate_password_hash(form.password1.data)
            u = Users(name=form.name.data, email=form.email.data, psw=hash)
            db.session.add(u)
            db.session.commit()
            flash("Вы успешно зарегистрированы", category="success")
            return redirect(url_for("auth.login"))
        except:
            flash("Что-то пошло не так.", category="danger")

    return render_template(
        "register.html",
        title="Регистрация",
        comment="Зарегистрируйтесь, пожалуйста",
        form=form,
    )


@bp.route("/login", methods=("POST", "GET"))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        UsrLog.login_attempt(form.email.data, request.remote_addr)
        uq = db.select(Users).filter(Users.email == form.email.data)
        user = db.session.execute(uq).scalar_one_or_none()

        if user:
            if check_password_hash(user.psw, form.password.data):
                rem = form.remember_me.data
                login_user(user, remember=rem)
                UsrLog.login(request.remote_addr)
                return redirect(request.args.get("next") or url_for("all.dashboard"))
            else:
                flash("Неверный пароль", category="danger")
        else:
            flash("Пользователь не существует", category="danger")
    return render_template("login.html", title="Вход", comment="Авторизация", form=form)


@bp.route("/logout", methods=("POST", "GET"))
@login_required
def logout():
    UsrLog.logout(request.remote_addr)
    logout_user()
    return redirect(url_for("all.index"))
