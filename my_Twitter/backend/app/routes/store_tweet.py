from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.tweet import TweetCreate, Tweet
from database.db import SessionLocal, engine, Tweet as TweetModel

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/store_tweet/", response_model=Tweet)
def create_tweet(tweet: TweetCreate, db: Session = Depends(get_db)):
    db_tweet = TweetModel(**tweet.dict())
    db.add(db_tweet)
    db.commit()
    db.refresh(db_tweet)
    return db_tweet
