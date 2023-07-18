from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine("sqlite:///test.db", echo=True)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    ...
