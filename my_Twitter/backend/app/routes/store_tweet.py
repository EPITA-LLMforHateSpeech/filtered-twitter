from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.tweet import TweetCreate, Tweet
from backend.database.db import SessionLocal, PostedSessionLocal
from backend.database.models import Tweet as TweetModel, PostedTweet as PostedTweetModel

router = APIRouter()

# Dependency for tweets database
def get_tweets_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency for posted tweets database
def get_posted_db():
    db = PostedSessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/store_tweet")
def store_tweet(tweet_id: str, user_id: str, db: Session = Depends(get_tweets_db), posted_db: Session = Depends(get_posted_db)):
    tweet = db.query(TweetModel).filter(TweetModel.tweet_id == tweet_id).first()
    if not tweet:
        raise HTTPException(status_code=404, detail=f"Tweet with ID {tweet_id} not found.")
    
    # Store the tweet in the posted tweets database
    posted_tweet = PostedTweetModel(
        tweet_id=tweet.tweet_id,
        retweet_id=tweet.retweet_id,
        user_id=user_id,
        tweet=tweet.tweet,
        likes=tweet.likes,
        retweets=tweet.retweets,
        safety_status=tweet.cnn_result
    )
    posted_db.add(posted_tweet)
    posted_db.commit()
    posted_db.refresh(posted_tweet)
    
    return {
        "tweet_id": posted_tweet.tweet_id,
        "retweet_id": posted_tweet.retweet_id,
        "user_id": posted_tweet.user_id,
        "tweet": posted_tweet.tweet,
        "likes": posted_tweet.likes,
        "retweets": posted_tweet.retweets,
        "safety_status": posted_tweet.safety_status
    }