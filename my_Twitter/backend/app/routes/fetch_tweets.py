from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.database.db import SessionLocal, Tweet as TweetModel
from backend.database.models import TweetSchema, StoredTweet as StoredTweetModel

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# For admin view
@router.get("/fetch_tweets", response_model=List[TweetSchema])
def fetch_tweets(db: Session = Depends(get_db)):
    tweets = db.query(TweetModel).all()
    return tweets


# For user view
@router.get("/display_tweets")
def display_tweets(db: Session = Depends(get_db)):
    tweets = db.query(StoredTweetModel).all()
    
    if not tweets:
        return {"message": "No tweets found"}
    
    return tweets