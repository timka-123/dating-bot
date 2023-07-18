from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine("sqlite:///test.db", echo=True)
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    ...

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    age = Column(Integer, nullable=False)
    city = Column(String, nullable=False)
    about = Column(String, nullable=False)
    name = Column(String, nullable=False)

User.metadata.create_all(bind=engine)
