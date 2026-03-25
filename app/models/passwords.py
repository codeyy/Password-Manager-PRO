from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship
from .database import Base

class PasswordEntry(Base):
    __tablename__ = "passwords"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password_encrypted = Column(LargeBinary, nullable=False)
    category = Column(String, nullable=False, server_default=text("'Not Specified'"))
    
    # Let the database handle the timestamps
    created_at = Column(String, default=text("STRFTIME('%d-%m-%Y %H-%M-%S', 'now', 'localtime')"))
    updated_at = Column(String, default=text("STRFTIME('%d-%m-%Y %H-%M-%S', 'now', 'localtime')"))

    # Link back to the user
    owner = relationship("User", back_populates="passwords")
    