from sqlalchemy import create_engine, Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from typing import Optional
from pydantic import BaseModel
from datetime import datetime, timezone

DATABASE_URL = "sqlite:///./filtered_tweets.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(String, unique=True, index=True)
    retweet_id = Column(String, nullable=True)
    tweet = Column(Text, nullable=False)
    user = Column(String, nullable=False)
    likes = Column(Integer, default=0)
    retweets = Column(Integer, default=0)
    logreg_prob = Column(Float, nullable=True)
    logreg_result = Column(Integer, nullable=True)
    logreg_prob = Column(Float, nullable=True)
    logreg_result = Column(Integer, nullable=True)
    cnn_prob = Column(Float, nullable=True)
    cnn_result = Column(Integer, nullable=True)
    admin_result = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))  # Timestamp for when the tweet was created


class StoredTweet(Base):
    __tablename__ = "stored_tweets"

    id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(String, unique=True, index=True)
    retweet_id = Column(String, nullable=True)
    user_id = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    text = Column(Text, nullable=False)
    likes = Column(Integer, default=0)
    retweets = Column(Integer, default=0)
    safety_status = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))  # Timestamp for when the tweet was stored

class ReportedTweet(Base):
    __tablename__ = "reported_tweets"

    id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(String, ForeignKey('tweets.tweet_id'), nullable=False)
    user_id = Column(String, nullable=False)
    reported_at = Column(DateTime, default=datetime.now(timezone.utc))  # Timestamp for when the safety status was changed


class SafetyStatusChange(Base):
    __tablename__ = "safety_status_changes"

    id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(String, ForeignKey('tweets.tweet_id'), nullable=False)
    new_safety_status = Column(Integer, nullable=False)
    change_source = Column(String, nullable=False)  # 'admin' or 'cnn'
    changed_at = Column(DateTime, default=datetime.now(timezone.utc))  # Timestamp for when the safety status was changed

Base.metadata.create_all(bind=engine)


# Pydantic models
class TweetSchema(BaseModel):
    tweet_id: str
    retweet_id: Optional[str] = None
    tweet: str
    user: str
    likes: int
    retweets: int
    logreg_prob: Optional[float] = None
    logreg_result: Optional[int] = None
    cnn_prob: Optional[float] = None
    cnn_result: Optional[int] = None
    admin_result: Optional[int] = None
    created_at: Optional[datetime] = None   # ISO format timestamp

    class Config:
        orm_mode = True

class StoreTweetSchema(BaseModel):
    tweet_id: str
    retweet_id: Optional[str] = None
    user_id: str
    text: str
    likes: int = 0
    retweets: int = 0
    safety_status: Optional[int] = None
    created_at: Optional[datetime] = None   # Include timestamp in the schema

    class Config:
        orm_mode = True

class ReportTweetSchema(BaseModel):
    tweet_id: str
    user_id: str
    safety_status: int
    reported_at: Optional[datetime] = None   # Include timestamp in the schema

    class Config:
        orm_mode = True

class UpdateSafetyStatus(BaseModel):
    tweet_id: str
    new_safety_status: int
    change_source: str
    changed_at: Optional[datetime] = None   # Include timestamp in the schema

    class Config:
        orm_mode = True