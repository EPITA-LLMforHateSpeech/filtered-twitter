
import logging
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from backend.app.routes import predict, health, store_tweet, report_tweet, fetch_tweets, tweets_query, interact
from backend.database.db import SessionLocal
from backend.database.models import Tweet as TweetModel 
from backend.app.utils.prediction_utils import request_batch_prediction, update_safety_status


app = FastAPI()

app.include_router(predict.router)
app.include_router(health.router)
app.include_router(store_tweet.router)
app.include_router(report_tweet.router)
app.include_router(fetch_tweets.router)
app.include_router(tweets_query.router)
app.include_router(interact.router)


# Schedule will change to 30 minutes in production
@app.on_event("startup")
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_and_predict_tweets, 'interval', seconds=30)
    scheduler.start()


@app.get("/")
def read_root():
    return {"message": "Welcome to the prediction API"}

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_and_predict_tweets():
    db = SessionLocal()
    try:
        tweets_to_predict = db.query(TweetModel).filter(TweetModel.cnn_prob.is_(None)).all()
        if tweets_to_predict:
            tweet_texts = [tweet.tweet for tweet in tweets_to_predict]
            tweet_ids = [tweet.tweet_id for tweet in tweets_to_predict]
            base_url = "http://localhost:8000" 
            results = request_batch_prediction(base_url, tweet_ids, tweet_texts)
            
            # Prepare the data for updating the safety status
            for result in results.get("results", []):
                if result['cnn_result'] == 1:
                    update_safety_status(base_url, result['tweet_id'], result['cnn_result'], change_source='cnn')

            logger.info(f"CNN predictions: {results}")

    finally:
        db.close()