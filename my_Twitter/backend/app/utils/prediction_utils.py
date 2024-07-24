import requests
from backend.database.db import Tweet as TweetModel
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


def prepare_batch_prediction_data(tweet_ids, texts):
    # Prepare data for the request
    return {
        "tweet_ids": tweet_ids,
        "texts": texts
    }

def request_batch_prediction(base_url, tweet_ids, texts):
    # Prepare the batch prediction data
    batch_data = prepare_batch_prediction_data(tweet_ids, texts)
    
    # Make the POST request
    response = requests.post(f'{base_url}/predict', json=batch_data)
    
    # Return the response JSON
    return response.json()

def update_safety_status(base_url, tweet_id, new_safety_status, change_source):
    update_data = {
        "tweet_id": tweet_id,
        "new_safety_status": new_safety_status,
        "change_source": change_source,
        "changed_at": datetime.now(timezone.utc).isoformat()  # Add current time

    }
    response = requests.post(f"{base_url}/update_safety_status", json=update_data)
    if response.status_code != 200:
        logger.error(f"Failed to update safety status for tweet ID {tweet_id}: {response.status_code} - {response.json()}")
