from sqlalchemy import Column, Integer, String

from .. import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    age = Column(Integer, nullable=False)
    city = Column(String, nullable=False)
    about = Column(String, nullable=False)
    name = Column(String, nullable=False)
