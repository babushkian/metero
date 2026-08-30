from flask_login import LoginManager
from .database import db
from .tables import Users

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    user = db.session.get(Users, user_id)
    return user
    # return Users.query.get(user_id)
