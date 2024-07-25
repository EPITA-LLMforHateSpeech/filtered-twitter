from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.db import SessionLocal
from backend.database.models import Tweet as TweetModel, SafetyStatusChange
from typing import List

router = APIRouter()

# Dependency to get the SQLAlchemy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/tweets/unsafe/{change_source}")
def get_unsafe_tweets(change_source: str, db: Session = Depends(get_db)):
    """
    Get unsafe tweets based on the change source ('admin' or 'cnn').
    """
    if change_source not in ['admin', 'cnn']:
        raise HTTPException(status_code=400, detail="Invalid change source")

    # Get tweet IDs from SafetyStatusChange table based on the change source
    unsafe_changes = db.query(SafetyStatusChange).filter(SafetyStatusChange.change_source == change_source).all()

    if not unsafe_changes:
        return {"message": "No unsafe tweets found for the given change source"}
    
    tweet_ids = [change.tweet_id for change in unsafe_changes]

    if not tweet_ids:
        raise HTTPException(status_code=404, detail="No unsafe tweets found")

    # Get the tweets from the Tweet table based on tweet IDs
    unsafe_tweets = db.query(TweetModel).filter(TweetModel.tweet_id.in_(tweet_ids)).all()

    return unsafe_tweets

@router.get("/tweets/risky")
def get_risky_tweets(db: Session = Depends(get_db)):
    """
    Get tweets with a CNN probability between 30% and 50%.
    """
    risky_tweets = db.query(TweetModel).filter(TweetModel.cnn_prob.between(0.30, 0.50)).all()
    
    if not risky_tweets:
        raise HTTPException(status_code=404, detail="No risky tweets found")

    return risky_tweets


# @router.get("/unsafe_changes", response_model=List[SafetyStatusChange])
# def get_unsafe_changes(change_source: str, db: Session = Depends(get_db)):
#     if change_source not in ["cnn", "admin"]:
#         raise HTTPException(status_code=400, detail="Invalid change source")
    
#     changes = db.query(SafetyStatusChange).filter(
#         SafetyStatusChange.change_source == change_source
#     ).all()
    
#     return changes