import datetime
from sqlalchemy import select
from app.model.tables import Meters
from app.repositories.base import BaseRepositiry
from flask_login import current_user


class MetersRepository(BaseRepositiry):
    def with_id(self, id_):
        print(id_, type(id_))
        q = select(Meters).where(Meters.id == id_)
        return self.session.execute(q).scalar()

    def with_current_user(
        self,
    ):
        q = select(Meters).filter(Meters.user_id == current_user.id)
        return self.session.execute(q).scalars().all()
