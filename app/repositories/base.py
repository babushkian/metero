from app.model.database import db


class BaseRepositiry:
    def __init__(self):
        self.session = db.session
