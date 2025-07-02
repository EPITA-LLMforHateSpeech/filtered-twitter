from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database.db import SessionLocal, Tweet as TweetModel
from backend.database.models import TweetSchema, StoredTweet as StoredTweetModel
from backend.database.models import TweetSchema, StoreTweetSchema
import requests
from datetime import datetime
from pydantic import BaseModel


router = APIRouter()

base_url = "http://localhost:8000"

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
@router.get("/fetch_tweet/{tweet_id}", response_model=TweetSchema)
def fetch_tweet(tweet_id: str, db: Session = Depends(get_db)):
    tweet = db.query(TweetModel).filter(TweetModel.tweet_id == tweet_id).first()
    
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

def post_tweet_for_prediction(tweet, user):
    response = requests.post(f'{base_url}/predict', json={"text": tweet, "user": user})
    return response.json()

def store_posted_tweet(tweet_id, retweet_id, user_id, text, likes, retweets, safety_status, created_at):
    data = {
        "tweet_id": tweet_id,
        "retweet_id": retweet_id,
        "user_id": user_id,
        "text": text,
        "likes": likes,
        "retweets": retweets,
        "safety_status": safety_status,
        "created_at": created_at
    }
    try:
        response = requests.post(f'{base_url}/store_tweet', json=data)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error storing posted tweet: {e}")
        return {"error": str(e)}

class UpdateTweetRequest(BaseModel):
    new_text: str
    user: str


@router.put("/update_tweet/{tweet_id}", response_model=TweetSchema)
def update_tweet(
    tweet_id: str,
    request: UpdateTweetRequest,  # Use schema here
    db: Session = Depends(get_db)
):
    # Fetch the tweet from StoredTweet table
    stored_tweet = db.query(StoredTweetModel).filter(StoredTweetModel.tweet_id == tweet_id).first()
    if not stored_tweet:
        raise HTTPException(status_code=404, detail="Tweet not found in stored tweets")

    # Fetch the tweet from Tweet table
    tweet = db.query(TweetModel).filter(TweetModel.tweet_id == tweet_id).first()
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found in tweets")

    # Perform prediction
    prediction = post_tweet_for_prediction(request.new_text, request.user)

    # Check prediction result
    if prediction.get("logreg_result") != 1:
        # Update text in StoredTweet
        stored_tweet.text = request.new_text
        
        # Update fields in Tweet
        tweet.logreg_prob = prediction.get("logreg_prob", None)
        tweet.logreg_result = prediction.get("logreg_result", None)
        tweet.cnn_prob = prediction.get("cnn_prob", None)
        tweet.cnn_result = None  # Reset CNN results

        # Commit changes
        db.commit()
        db.refresh(stored_tweet)  # Refresh to get updated data
        db.refresh(tweet)  # Refresh to get updated data
        return {"message": "Tweet updated successfully", "updated_tweet": tweet}
    else:
        raise HTTPException(status_code=402, detail="Tweet was flagged by logistic regression and not updated")
    

@router.delete("/delete_tweet/{tweet_id}")
def delete_tweet(tweet_id: str, db: Session = Depends(get_db)):
    # Fetch the tweet from StoredTweet table
    tweet = db.query(StoredTweetModel).filter(StoredTweetModel.tweet_id == tweet_id).first()
    
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    
    # Delete the tweet
    db.delete(tweet)
    db.commit()
    
    return {"message": "Tweet deleted successfully"}
