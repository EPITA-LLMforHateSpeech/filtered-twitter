from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database.db import SessionLocal, Tweet as TweetModel
from backend.database.models import TweetSchema, StoredTweet as StoredTweetModel
from backend.database.models import TweetSchema, StoreTweetSchema

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

# Fetch tweet by ID
@router.get("/fetch_tweet/{tweet_id}", response_model=StoreTweetSchema)
def fetch_tweet(tweet_id: str, db: Session = Depends(get_db)):
    tweet = db.query(StoredTweetModel).filter(StoredTweetModel.tweet_id == tweet_id).first()
    
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    
    return tweet


# Fetch tweets by username
@router.get("/fetch_tweets_by_user/{username}", response_model=List[StoreTweetSchema])
def fetch_tweets_by_user(username: str, db: Session = Depends(get_db)):
    tweets = db.query(StoredTweetModel).filter(StoredTweetModel.user_id == username).all()
    
    if not tweets:
        raise HTTPException(status_code=404, detail="No tweets found for the given username")
    
    return tweets
