import os
import datetime
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask


from flask_cors import cross_origin
from flask_login import login_required, login_user, logout_user
from wtforms import Label
from sqlalchemy import exists, distinct, and_


from app.model import db, login_manager


load_dotenv(override=True)

# Получаем URL из переменной окружения
DATABASE_URL = os.getenv("DATABASE_URL")


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["FLASK_DEBUG"] = True

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.login_message = "Для внесения показаний нужно авторизоваться."
    login_manager.login_message_category = "danger"

    from app.routes import bp

    app.register_blueprint(bp)
    return app
