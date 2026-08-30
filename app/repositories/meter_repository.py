import datetime
from collections.abc import Sequence

from flask_login import current_user
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.model.tables import Meters


class MetersRepository:

    def __init__(self, session: Session) -> None:
        self.session = session

    def with_id(self, id_)-> Meters | None:
        """Возвращает счетчик по его идентификатору."""
        print(id_, type(id_))
        q = select(Meters).where(Meters.id == id_)
        return self.session.execute(q).scalar()

    def with_current_user(self) -> Sequence[Meters]:
        q = select(Meters).filter(Meters.user_id == current_user.id)
        return self.session.execute(q).scalars().all()

    def get_max_order(self, user_id: int)-> int | None:
        """Возвращает самое большое значение order среди счетчиков данного пользователя.

        Это нужно, чтобы поставить новый счетчик в конце списка.
        """
        q = select(func.max(Meters.order)).where(Meters.user_id == user_id)
        return  self.session.execute(q).scalar()