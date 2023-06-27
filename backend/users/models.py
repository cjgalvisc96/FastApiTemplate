from datetime import datetime

from sqlalchemy import Column, String, Boolean, Integer, DateTime

from backend.shared.sqlalchemy_repository import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    lastname = Column(String(100))
    email = Column(String(50), unique=True)
    hashed_password = Column(String(250))
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return (
            f"<User(id={self.id}, "
            f"name=\"{self.name}\", "
            f"lastname=\"{self.lastname}\", "
            f"email=\"{self.email}\", "
            f"hashed_password=\"{self.hashed_password}\", "
            f"active={self.active})>"
        )
