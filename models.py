from sqlalchemy import Column, String, Integer
from database import Base


class User(Base):
    __tablename__ = "new_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hash_password = Column(String)
