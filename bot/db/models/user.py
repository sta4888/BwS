from sqlalchemy import BigInteger, String, Column, Integer, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.db.base import Base



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # локальный id
    user_id = Column(Integer, unique=True, index=True)  # Telegram user ID
    username = Column(String(255), nullable=True)       # ник в Telegram
    first_name = Column(String(255), nullable=True)     # имя
    last_name = Column(String(255), nullable=True)      # фамилия
    balance = Column(DECIMAL(10, 2), default=0)         # баланс пользователя

    votes = relationship("Vote", back_populates="user")


