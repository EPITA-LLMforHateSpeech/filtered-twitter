from sqlalchemy import Column, Integer, String, Float, Text
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
    linreg_prob = Column(Float, nullable=True)
    linreg_result = Column(Integer, nullable=True)
    cnn_prob = Column(Float, nullable=True)
    cnn_result = Column(Integer, nullable=True)
    admin_result = Column(Integer, nullable=True)

class PostedTweet(Base):
    __tablename__ = "posted_tweets"

    id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(String, unique=True, index=True)
    retweet_id = Column(String, nullable=True)
    user_id = Column(String, nullable=False)
    tweet = Column(Text, nullable=False)
    likes = Column(Integer, default=0)
    retweets = Column(Integer, default=0)
    safety_status = Column(Integer, nullable=False)
