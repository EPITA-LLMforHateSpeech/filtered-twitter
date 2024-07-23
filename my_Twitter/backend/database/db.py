from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./tweets.db"
POSTED_DATABASE_URL = "sqlite:///./posted_tweets.db"


engine = create_engine(DATABASE_URL)
PostedEngine = create_engine(POSTED_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
PostedSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=PostedEngine)

Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)
    Base.metadata.create_all(bind=PostedEngine)

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

Base.metadata.create_all(bind=engine)
