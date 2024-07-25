from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .db import Base

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
    cnn_prob = Column(Float, nullable=True)
    cnn_result = Column(Integer, nullable=True)
    admin_result = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

class StoredTweet(Base):
    __tablename__ = "stored_tweets"

    id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(String, unique=True, index=True)
    retweet_id = Column(String, nullable=True)
    user_id = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    likes = Column(Integer, default=0)
    retweets = Column(Integer, default=0)
    safety_status = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

class ReportedTweet(Base):
    __tablename__ = "reported_tweets"

    id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(String, ForeignKey('tweets.tweet_id'), nullable=False)
    user_id = Column(String, nullable=False)
    reported_at = Column(DateTime, default=datetime.now(timezone.utc))

class SafetyStatusChange(Base):
    __tablename__ = "safety_status_changes"

    id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(String, ForeignKey('tweets.tweet_id'), nullable=False)
    new_safety_status = Column(Integer, nullable=False)
    change_source = Column(String, nullable=False)

class UpdateSafetyStatus(Base):
    __tablename__ = "safety_status_changes"  # Ensure the table name is correct

    id = Column(Integer, primary_key=True, index=True)  # Add an ID column if needed
    tweet_id = Column(String, ForeignKey('tweets.tweet_id'), nullable=False)
    new_safety_status = Column(Integer, nullable=False)
    change_source = Column(String, nullable=False)
    changed_at = Column(DateTime, default=datetime.now(timezone.utc))
    __table_args__ = {"extend_existing": True}

# class Config:
#     orm_mode = True