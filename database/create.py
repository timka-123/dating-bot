from .core import engine, Session
from .models import User


def create_user(user_id: int, name: str, age: int, about: str, city: str, photo_link: str) -> User:
    with Session(autoflush=False, bind=engine) as db:
        user = User(id=user_id, name=name, age=age, about=about, city=city, photo_link=photo_link)
        db.add(user)
        db.commit()
        return user
