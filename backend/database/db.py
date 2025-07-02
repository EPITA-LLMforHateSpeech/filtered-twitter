from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.database.models import Base, Tweet  # Import the Tweet model

DATABASE_URL = "sqlite:///./filtered_tweets.db"  # Update with your database URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
Base.metadata.create_all(bind=engine)

# class Tweet(Base):
#     __tablename__ = "tweets"

#     id = Column(Integer, primary_key=True, index=True)
#     tweet_id = Column(String, unique=True, index=True)
#     retweet_id = Column(String, nullable=True)
#     tweet = Column(Text, nullable=False)
#     user = Column(String, nullable=False)
#     likes = Column(Integer, default=0)
#     retweets = Column(Integer, default=0)
#     logreg_prob = Column(Float, nullable=True)
#     logreg_result = Column(Integer, nullable=True)
#     cnn_prob = Column(Float, nullable=True)
#     cnn_result = Column(Integer, nullable=True)
#     admin_result = Column(Integer, nullable=True)

# Base.metadata.create_all(bind=engine)
