import datetime
from sqlalchemy import select
from app.model.tables import Dates
from app.repositories.base import BaseRepositiry


class DateRepository(BaseRepositiry):
    def date_id_exists(self, date_id: int) -> bool:
        date_id_query = select(Dates).where(Dates.id == date_id)
        res = self.session.execute(date_id_query).scalar_one_or_none()
        return res is not None

    def date_exists(self, date: datetime.date):
        date_query = select(Dates).where(Dates.date == date)
        date_obj = self.session.execute(date_query).scalar_one_or_none()
        return date_obj

    def get_edited_date_id(self, conv_date: datetime.date) -> int:
        date_id = self.date_exists(conv_date)
        if date_id is None:
            date_id = Dates(date=conv_date)
            self.session.add(date_id)
            self.session.commit()
        return date_id.id
