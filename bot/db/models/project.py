from sqlalchemy import BigInteger, String, Column, Integer, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.db.base import Base



class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)  # название проекта
    total_votes = Column(Integer, default=0)    # общее количество голосов в заказе
    given_votes = Column(Integer, default=0)    # количество голосов отданных
    confirmed_votes = Column(Integer, default=0)  # количество подтвержденных голосов

    votes = relationship("Vote", back_populates="project")