
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.model.tables import Users


class UserRepository:

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, user_dict: dict) -> Users:
        u = Users(**user_dict)
        self.session.add(u)
        return u

    def get_by_email(self, email: str) -> Users | None:
        stmt = select(Users).where(Users.email == email)
        result = self.session.scalars(stmt)
        return result.one_or_none()