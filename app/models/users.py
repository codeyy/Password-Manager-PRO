from sqlalchemy import Column, Integer, String, LargeBinary
from app.models.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    salt = Column(LargeBinary) # BLOB in SQLite maps to LargeBinary

    # This allows you to access a user's passwords easily: user.passwords
    passwords = relationship("PasswordEntry", back_populates="owner")

