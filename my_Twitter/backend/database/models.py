from sqlalchemy import create_engine, Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DATABASE_URL = "sqlite:///./tweets.db"

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
    cnn_prob = Column(Float, nullable=True)
    cnn_result = Column(Integer, nullable=True)
    admin_result = Column(Integer, nullable=True)

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

class ReportedTweet(Base):
    __tablename__ = "reported_tweets"

    id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(String, ForeignKey('tweets.tweet_id'), nullable=False)
    user_id = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)
