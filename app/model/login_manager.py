from flask_login import LoginManager
from .database import SessionLocal
from .tables import Users

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    with SessionLocal() as session:
        user = session.get(Users, user_id)
    return user
