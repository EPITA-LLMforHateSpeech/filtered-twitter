from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Union, List
import pickle
from tensorflow.keras.models import load_model
from backend.app.utils.preprocess import preprocess_tfidf, preprocess_cnn
from backend.database.db import SessionLocal, Tweet as TweetModel
import joblib
from sqlalchemy.orm import Session
import os
import hashlib


router = APIRouter()

# Load the models
script_dir = os.path.dirname(__file__)

# Define absolute paths based on script directory
logreg_model_path = os.path.join(script_dir, '..\\..\\models\\logistic_regression_model.pkl')
cnn_model_path = os.path.join(script_dir, '..\\..\\models\\cnn_model_regularization.keras')


logreg_model = joblib.load(logreg_model_path)
cnn_model = load_model(cnn_model_path)

class SingleTextData(BaseModel):
    text: str

class BatchTextData(BaseModel):
    tweet_ids: List[str]  # List of tweet IDs
    texts: List[str]

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_tweet_id(text: str) -> str:
    sha256_hash = hashlib.sha256(text.encode()).hexdigest() # Create a SHA-256 hash of the text
    tweet_id = sha256_hash[:8] # Take the first 8 characters of the hash (32 bits)
    return tweet_id


@router.post("/predict")
def predict(data: Union[SingleTextData, BatchTextData], db: Session = Depends(get_db)):
    if isinstance(data, SingleTextData):
        text_data = [data.text]

        # Preprocess for TF-IDF and make predictions
        X_tfidf = preprocess_tfidf(text_data)
        logreg_pred = logreg_model.predict(X_tfidf)[0]
        logreg_prob = logreg_model.predict_proba(X_tfidf)[0][1] # Extract probability of being 1

        # Generate unique tweet_id based on text content
        tweet_id = generate_tweet_id(data.text)

        # Attempt to find an existing tweet
        tweet = db.query(TweetModel).filter(TweetModel.tweet_id == tweet_id).first()
        
        if tweet:
            # Update existing tweet
            tweet.linreg_prob = logreg_prob
            tweet.linreg_result = int(logreg_pred)
        else:
            # Insert new tweet if not found
            tweet = TweetModel(
                tweet_id=tweet_id,
                tweet=data.text,
                user="some_user",
                likes=0,
                retweets=0,
                linreg_prob=logreg_prob,
                linreg_result=int(logreg_pred),
                cnn_prob=None,  # No CNN prediction for single requests
                cnn_result=None
            )
            db.add(tweet)
        
        db.commit()
        db.refresh(tweet)
        
        return {
            "tweet_id": tweet_id,
            "tweet": data.text,
            "user": "some_user",
            "likes": 0,
            "retweets": 0,
            "linreg_prob": float(logreg_prob),  # Convert numpy.float32 to float
            "linreg_result": int(logreg_pred),
            "cnn_prob": None,
            "cnn_result": None
        }
     
    elif isinstance(data, BatchTextData):
        if len(data.texts) != len(data.tweet_ids):
            raise HTTPException(status_code=400, detail="Texts and tweet_ids must have the same length.")
        
        text_data = data.texts
        tweet_ids = data.tweet_ids
        
        # Preprocess for CNN and make predictions
        X_cnn = preprocess_cnn(text_data)
        cnn_preds = cnn_model.predict(X_cnn)
        
        results = []
        for i, tweet_id in enumerate(tweet_ids):
            tweet = db.query(TweetModel).filter(TweetModel.tweet_id == tweet_id).first()
            if tweet is None:
                raise HTTPException(status_code=404, detail=f"Tweet with ID {tweet_id} not found.")
            
            cnn_pred = cnn_preds[i]
            cnn_prob = float(max(cnn_pred[0], 1 - cnn_pred[0]))  # Convert numpy.float32 to float
            cnn_result = int(cnn_pred[0] > 0.5)
            
            # Update existing tweet in database
            tweet.cnn_prob = cnn_prob
            tweet.cnn_result = cnn_result
            db.commit()
            db.refresh(tweet)
            
            # Append result to the list
            results.append({
                "tweet_id": tweet_id,
                "tweet": tweet.tweet,
                "user": tweet.user,
                "likes": tweet.likes,
                "retweets": tweet.retweets,
                "linreg_prob": float(tweet.linreg_prob),  # Convert numpy.float32 to float
                "linreg_result": tweet.linreg_result,
                "cnn_prob": cnn_prob,
                "cnn_result": cnn_result
            })
        
        return {"results": results}