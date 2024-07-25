from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.database.db import SessionLocal
from backend.database.models import Tweet as TweetModel, StoredTweet, UserTweetInteraction
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import os
import hashlib
import datetime
import random
import requests


router = APIRouter()

base_url = "http://localhost:8000"


class LikeRequest(BaseModel):
    user_id: str

class RetweetRequest(BaseModel):
    user_id: str
    text: str

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() # Dependency for total tweets


def generate_tweet_id(text: str, user:str) -> str:
    random_int = str(random.randint(0, 1_000_000))
    
    # Combine text, user, and random integer into one string
    combined_string = text + user + random_int
    
    # Create a hash from the combined string
    tweet_id = hashlib.sha256(combined_string.encode()).hexdigest()
    
    return tweet_id

@router.post("/like_tweet/{tweet_id}")
def like_tweet(tweet_id: str, request: LikeRequest, db: Session = Depends(get_db)):
    user_id = request.user_id
    
    # Find the tweet in both tables
    tweet = db.query(TweetModel).filter(TweetModel.tweet_id == tweet_id).first()
    stored_tweet = db.query(StoredTweet).filter(StoredTweet.tweet_id == tweet_id).first()
    
    if not tweet or not stored_tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")

    # Update likes count in both tables
    tweet.likes += 1
    stored_tweet.likes += 1

    # Save interaction
    interaction = UserTweetInteraction(
        user_id=user_id,
        tweet_id=tweet_id,
        interaction_type="like"
    )
    
    db.add(tweet)
    db.add(stored_tweet)
    db.add(interaction)
    db.commit()
    
    return {"message": "Tweet liked successfully"}

@router.post("/retweet/{tweet_id}")
def retweet(tweet_id: str, request: RetweetRequest, db: Session = Depends(get_db)):
    user_id = request.user_id
    text = request.text

    # Find the original tweet
    original_tweet = db.query(TweetModel).filter(TweetModel.tweet_id == tweet_id).first()
    stored_original_tweet = db.query(StoredTweet).filter(StoredTweet.tweet_id == tweet_id).first()

    if not original_tweet or not stored_original_tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")

    # Increment the retweet count for the original tweet in both tables
    original_tweet.retweets += 1
    stored_original_tweet.retweets += 1
    db.add(original_tweet)
    db.add(stored_original_tweet)
    db.commit()

    # Predict and store the retweet using external services
    prediction = post_tweet_for_prediction(text, user_id)
    
    if prediction["logreg_result"] != 1:
        created_at=datetime.datetime.now(datetime.timezone.utc),  # Use timezone-aware UTC datetime

        store_response = store_posted_tweet(
            tweet_id=prediction["tweet_id"],
            retweet_id=tweet_id,
            user_id=user_id,
            text=text,
            likes=0,
            retweets=0,
            safety_status=None,  # Initial safety status is None
            created_at=created_at
        )
        print("Store Tweet Response:", store_response)

        # Save interaction
        interaction = UserTweetInteraction(
            user_id=user_id,
            tweet_id=prediction["tweet_id"],
            interaction_type="retweet"
        )
        db.add(interaction)
        db.commit()
        
        return {"message": "Tweet retweeted successfully", "new_tweet_id": prediction["tweet_id"]}

    return {"message": "Tweet was flagged by logistic regression and not stored"}

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
    response = requests.post(f'{base_url}/store_tweet', json=data)
    return response.json()