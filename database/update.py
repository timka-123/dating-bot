from .core import Session, engine
from .models import User


def update_user_info(user_id: int, key: str, value: str) -> User:
    with Session(autoflush=False, bind=engine) as db:
        user = db.get(User, user_id)
        match key:
            case "name": user.name = value
            case "age": user.age = int(value)
            case "about": user.about = value
            case "photo": user.photo_link = value
            case "city": user.city = value
        db.commit()
        return user
