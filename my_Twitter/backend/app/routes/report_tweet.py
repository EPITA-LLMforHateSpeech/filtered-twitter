# backend/app/routes/report_tweet.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.db import SessionLocal
from backend.database.models import Tweet as TweetModel, ReportTweetSchema, ReportedTweet as ReportedTweetModel

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/report_tweet")
def report_tweet(report: ReportTweetSchema, db: Session = Depends(get_db)):
    tweet = db.query(TweetModel).filter(TweetModel.tweet_id == report.tweet_id).first()
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")

    # Save the report in the reported_tweets table
    reported_tweet = ReportedTweetModel(
        tweet_id=report.tweet_id,
        user_id=report.user_id
    )
    db.add(reported_tweet)
    db.commit()

    return {"message": "Tweet reported successfully"}

@router.get("/reported_tweets")
def get_reported_tweets(db: Session = Depends(get_db)):
    reported_tweets = db.query(ReportedTweetModel).all()
    
    if not reported_tweets:
        raise HTTPException(status_code=404, detail="No reported tweets found")
    
    return reported_tweets