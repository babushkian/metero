import datetime
from typing import Sequence
from sqlalchemy import select
from app.model.tables import Measures
from app.repositories.base import BaseRepositiry
from flask_login import current_user


class MeasureRepository(BaseRepositiry):
    def with_date_id(self, date_id: int) -> Sequence[Measures]:
        q = (
            select(Measures)
            .where(Measures.user_id == current_user.id)
            .where(Measures.date_id == date_id)
        )
        msmnts = self.session.execute(q).scalars().all()
        return msmnts

    def specific_record(self, date, meter) -> Measures | None:
        q = (
            select(Measures)
            .where(Measures.user_id == current_user.id)
            .where(Measures.date_id == date)
            .where(Measures.meter_id == meter)
        )
        measurement = self.session.execute(q).scalar_one_or_none()
        return measurement
