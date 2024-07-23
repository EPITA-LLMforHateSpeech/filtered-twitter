from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.database.db import SessionLocal
from backend.database.models import StoredTweet, Tweet as TweetModel

router = APIRouter()

class StoreTweetData(BaseModel):
    tweet_id: str
    user_id: str

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/store_tweet")
def store_tweet(data: StoreTweetData, db: Session = Depends(get_db)):
    # Retrieve the original tweet from the main tweets table
    original_tweet = db.query(TweetModel).filter(TweetModel.tweet_id == data.tweet_id).first()

    # Find the original tweet
    if original_tweet is None:
        print(f"Storing tweet: Tweet with tweet_id {data.tweet_id} not found in tweets table. This probably means that prediction has failed.")
        raise HTTPException(status_code=404, detail="Original tweet not found.")
    
    # Insert the tweet into the stored_tweets table
    stored_tweet = StoredTweet(
        tweet_id=data.tweet_id,
        retweet_id=original_tweet.retweet_id,  # Handle None values
        user_id=data.user_id,
        text=original_tweet.tweet,
        likes=original_tweet.likes,
        retweets=original_tweet.retweets,
        safety_status=original_tweet.cnn_result  # Assuming safety_status is derived from CNN result
    )
    db.add(stored_tweet)
    db.commit()
    db.refresh(stored_tweet)
    return stored_tweet
