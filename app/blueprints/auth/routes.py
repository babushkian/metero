from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.blueprints.main.forms import LoginForm, RegisterForm
from app.model import SessionLocal
from app.repositories import UserRepository

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.get("/register")
def register_user():
    form = RegisterForm()
    return render_template(
        "register.html",
        title="Регистрация",
        comment="Зарегистрируйтесь, пожалуйста",
        form=form,
    )


@bp.post("/register")
def create_new_user():
    form = RegisterForm()
    if form.validate_on_submit():
        with SessionLocal() as session:
            ur = UserRepository(session)
            user = ur.get_by_email(form.email.data)

            if user:
                flash(
                    "Пользователь с таким почтовым адресом уже существует",
                    category="danger",
                )
                return redirect(url_for("auth.register_user"))
            try:
                psw_hash = generate_password_hash(form.password1.data)
                new_user = ur.add({"email": form.email.data, "name": form.name.data, "psw": psw_hash})
                session.commit()
                flash("Вы успешно зарегистрированы", category="success")
                return redirect(url_for("auth.login"))
            except Exception:
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
    if request.method == "POST" and form.validate_on_submit():
        with SessionLocal() as session:
            ur = UserRepository(session)
            user = ur.get_by_email(form.email.data)
        if user:
            if check_password_hash(user.psw, form.password.data):
                rem = form.remember_me.data
                login_user(user, remember=rem)
                return redirect(request.args.get("next") or url_for("all.dashboard"))
            else:
                flash("Неверный пароль", category="danger")
        else:
            flash("Пользователь не существует", category="danger")
    return render_template("login.html", title="Вход", comment="Авторизация", form=form)


@bp.route("/logout", methods=("POST", "GET"))
@login_required
def logout():
    logout_user()
    return redirect(url_for("all.index"))
