from typing import List

from . import User
from .core import Session, engine


def get_user(user_id: int) -> User:
    with Session(autoflush=False, bind=engine) as db:
        user = db.get(User, user_id)
        return user


def get_users(city: str, user_id: int) -> List[User]:
    with Session(autoflush=False, bind=engine) as db:
        users = db.query(User).filter_by(city=city).all()
        for user in users:
            if user.id == user_id:
                del users[users.index(user)]
        return users
