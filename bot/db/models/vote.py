from sqlalchemy import BigInteger, String, Column, Integer, DECIMAL, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.db.base import Base


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    phone_number = Column(String(20), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"))
    sms_code = Column(String(10), nullable=True)
    confirm_code = Column(String(10), nullable=True)
    is_confirmed = Column(Boolean, default=False)  # подтвержден или нет

    user = relationship("User", back_populates="votes")
    project = relationship("Project", back_populates="votes")