from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, DECIMAL
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # локальный id
    user_id = Column(Integer, unique=True, index=True)  # Telegram user ID
    username = Column(String(255), nullable=True)       # ник в Telegram
    first_name = Column(String(255), nullable=True)     # имя
    last_name = Column(String(255), nullable=True)      # фамилия
    balance = Column(DECIMAL(10, 2), default=0)         # баланс пользователя

    votes = relationship("Vote", back_populates="user")


class AdminData(Base):
    __tablename__ = "admin_data"

    id = Column(Integer, primary_key=True)
    broadcast_message = Column(Text, nullable=True)   # сообщение рассылки
    min_withdraw = Column(DECIMAL(10, 2), default=0)  # минимальный баланс для вывода
    withdraw_type = Column(String(50), default="uc")  # тип вывода: "uc" или "card"


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)  # название права


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)  # название проекта
    total_votes = Column(Integer, default=0)    # общее количество голосов в заказе
    given_votes = Column(Integer, default=0)    # количество голосов отданных
    confirmed_votes = Column(Integer, default=0)  # количество подтвержденных голосов

    votes = relationship("Vote", back_populates="project")


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
