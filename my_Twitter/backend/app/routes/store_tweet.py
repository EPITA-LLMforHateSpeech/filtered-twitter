from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.database.db import SessionLocal
from backend.database.models import StoredTweet as StoredTweetModel, Tweet as TweetModel, UpdateSafetyStatus, SafetyStatusChange

router = APIRouter()

class UpdateSafetyStatus(BaseModel):
    tweet_id: str
    new_safety_status: int
    change_source: str  # 'cnn' or 'admin'

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
    stored_tweet = StoredTweetModel(
        tweet_id=data.tweet_id,
        retweet_id=original_tweet.retweet_id,
        user_id=data.user_id,
        text=original_tweet.tweet,
        likes=original_tweet.likes,
        retweets=original_tweet.retweets,
        safety_status=original_tweet.cnn_result
    )
    db.add(stored_tweet)
    db.commit()
    db.refresh(stored_tweet)
    return stored_tweet

@router.post("/update_safety_status")
def update_safety_status(data: UpdateSafetyStatus, db: Session = Depends(get_db)):
    tweet = db.query(TweetModel).filter(TweetModel.tweet_id == data.tweet_id).first()
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    
    # Update StoredTweetModel
    stored_tweet = db.query(StoredTweetModel).filter(StoredTweetModel.tweet_id == data.tweet_id).first()
    if stored_tweet:
        stored_tweet.safety_status = data.new_safety_status
    else:
        raise HTTPException(status_code=404, detail="Stored tweet not found")

    # Update the admin result if the caller is admin
    if data.change_source == 'admin':
        tweet.admin_result = data.new_safety_status

    # Log the change
    safety_status_change = SafetyStatusChange(
        tweet_id=data.tweet_id,
        new_safety_status=data.new_safety_status,
        change_source=data.change_source
    )
    db.add(safety_status_change)
    
    db.commit()
    db.refresh(tweet)
    
    return {"message": "Safety status updated successfully"}

@router.get("/safety_status_changes")
def get_safety_status_changes(db: Session = Depends(get_db)):
    # Fetch records from the SafetyStatusChange model
    status_changes = db.query(SafetyStatusChange).all()
    
    if not status_changes:
        raise HTTPException(status_code=404, detail="No safety status changes found")
    
    return status_changes