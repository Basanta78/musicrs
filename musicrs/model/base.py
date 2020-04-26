""" Base models of the database tables """

from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserProfile(Base):
    __tablename__ = "user_profile"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    user_name = Column(String(100), nullable=False)
    video_id = Column(String, nullable=True)
    audio_encoding = Column(String, nullable=True)
    created_date = Column(TIMESTAMP(timezone=True), default=func.now())
    updated_date = Column(TIMESTAMP(timezone=True), onupdate=func.now())


class Inference(Base):
    __tablename__ = "inference"

    id = Column(Integer, primary_key=True)
    video_id = Column(String, nullable=True)
    audio_encoding = Column(String, nullable=True)


class Recommendation(Base):
    __tablename__ = "recommend"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    recommended_url = Column(String, nullable=True)
