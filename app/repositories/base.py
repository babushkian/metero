from app.model.extensions import db


class BaseRepositiry:
    def __init__(self):
        self.session = db.session
