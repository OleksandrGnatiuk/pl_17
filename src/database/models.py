from datetime import datetime
import enum
from typing import List
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Enum, Integer, func, Float
from sqlalchemy.orm import declarative_base, relationship, mapped_column, Mapped
from src.database.db import engine


Base = declarative_base()


class Role(enum.Enum):
    admin = 'admin'
    moderator = 'moderator'
    user = 'user'


class Country(Base):
    __tablename__ = "countries"

    country_id = Column(Integer, primary_key=True)
    country_ukr = Column(String(255), nullable=False)
    country_eng = Column(String(255), nullable=False)
    cities = relationship("City", backref="country")

    def __str__(self):
        return self.country_eng


class City(Base):
    __tablename__ = "cities"

    city_id = Column(Integer, primary_key=True)
    city_ukr = Column(String(255), nullable=False)
    city_eng = Column(String(255), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.country_id"), nullable=False)
    users = relationship("User", backref="city")

    def __str__(self):
        return self.city_eng


class User(Base):
    __tablename__ = "users"

    # user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, primary_key=True)
    user_role = Column('role', Enum(Role), default=Role.user)
    password = Column(String(255), nullable=False)
    name = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    country_id = Column(Integer, ForeignKey("countries.country_id"), nullable=False)
    city_id = Column(Integer, ForeignKey("cities.city_id"), nullable=False)
    phone = Column(String(255))
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
    banned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __str__(self):
        return f"User id: {self.user_id}"


class Admin(User):
    __tablename__ = 'admin'
    admin_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    is_active = Column(Boolean, default=False)
    last_visit = Column(DateTime, default=func.now())


class SubscribePlan(Base):
    __tablename__ = 'subscribe_plans'
    plan_id = Column(Integer, primary_key=True, index=True)
    subscribe_plan = Column(String, nullable=False)
    plan_period = Column(Integer, nullable=False)


class MasterInfo(User):
    __tablename__ = 'master_info'
    master_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False, index=True)
    description = Column(String, nullable=True)
    salon_name = Column(String, nullable=True)
    salon_address = Column(String, nullable=True)
    longitude = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)
    is_active = Column(Boolean, default=False)
    plan_id = Column(Integer, ForeignKey('subscribe_plans.plan_id'))
    free_period = Column(Integer, nullable=True)
    plan_period = Column(Integer, nullable=True)
    subscribe_plan_rel = relationship("SubscribePlan", foreign_keys=[plan_id], backref="master_info")


class WorkPhoto(Base):
    __tablename__ = 'work_photos'
    work_photo_id = Column(Integer, primary_key=True, index=True)
    master_id = Column(Integer, ForeignKey('master_info.master_id'), nullable=False)
    work_photo_url = Column(String, nullable=True)


Base.metadata.create_all(bind=engine)
