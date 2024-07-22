# Twitter Text Classification

## Project Overview

This project involves building a text classification system designed to detect hate speech in tweets. The system includes a FastAPI backend for serving predictions and a Streamlit web app for interacting with the predictions. The models used are Logistic Regression for real-time predictions and Convolutional Neural Networks (CNN) for batch predictions. The data is stored in an SQLite database.

## Project Structure

```
my_Twitter/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── predict.py
│   │   │   ├── store_tweet.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── tweet.py
│   │   ├── utils/
│   │       ├── __init__.py
│   │       ├── preprocess.py
│   │
│   └── models/
│   │   ├── cnn_model_regularization.keras
│   │   ├── logistic_regression_model.joblib
│   │   ├── tfidf_vectorizer.joblib
│   │   └── tokenizer.pickle
│   │
│   └── database/
│       ├── db.py
│
├── data/
│   ├── test.csv
│
├── streamlit/
│   ├── app.py
│   ├── ...
│
└── tests/
    ├── test_predictions.py
    └── test_utils.py
```

## Prerequisites

- Python 3.11 or later
- FastAPI
- Uvicorn
- TensorFlow
- scikit-learn
- Pandas
- SQLite
- Joblib
- Pickle

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/EPITA-LLMforHateSpeech/my_twitter.git
   cd my_twitter/my_Twitter
   ```

2. **Create and activate a virtual environment:**

   ```sh
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install the required packages:**

   ```sh
   pip install -r requirements.txt
   ```

## Project Details

### Models

1. **Logistic Regression Model:**

   - Used for real-time predictions.
   - Stored as `logistic_regression_model.joblib`.

2. **CNN Model:**

   - Used for batch predictions.
   - Stored as `cnn_model_regularization.keras`.

3. **TF-IDF Vectorizer:**

   - Used for feature extraction in logistic regression.
   - Stored as `tfidf_vectorizer.joblib`.

4. **Tokenizer:**
   - Used for text preprocessing in CNN.
   - Stored as `tokenizer.pickle`.

### Backend (FastAPI)

1. **`main.py`:**

   - Entry point for the FastAPI application.

2. **`routes/predict.py`:**

   - Contains the `/predict` endpoint for both single and batch predictions.

3. **`schemas/predict_schemas.py`:**

   - Defines data schemas for prediction requests.

4. **`utils/preprocess.py`:**

   - Contains preprocessing functions for TF-IDF and CNN models.

5. **Database:**
   - SQLite database `tweets.db` used for storing tweet data.
   - Table: `tweets`

### Frontend (Streamlit) [incomplete implementation]

1. **`app.py`:**
   - Streamlit web app for interacting with the prediction API.

### Tests [incomplete implementation]

1. **`test_predictions.py`:**

   - Contains tests for prediction functions.

2. **`test_utils.py`:**
   - Contains tests for utility functions.

## Running the Project

### Start FastAPI Backend

1. Navigate to the `backend` directory:

   ```sh
   cd filtered-twitter/my_Twitter
   ```

2. Run the FastAPI server:

   ```sh
   uvicorn backend.app.main:app --reload
   ```

   The server will be available at `http://127.0.0.1:8000`.

### Start Streamlit Web App

1. Navigate to the `streamlit` directory:

   ```sh
   cd my_twitter/streamlit
   ```

2. Run the Streamlit app:

   ```sh
   streamlit run app.py
   ```

### Making Predictions

#### Single Prediction

Use the FastAPI `/predict` endpoint with a POST request containing the tweet text.

Example request:

```python
import requests

def predict_single(text):
    response = requests.post('http://127.0.0.1:8000/predict', json={'text': text})
    return response.json()

# Example usage
single_prediction = predict_single("Sample tweet text")
print("Single Prediction:", single_prediction)
```

#### Batch Prediction

Use the FastAPI `/predict` endpoint with a POST request containing a list of tweets and their IDs.

Example request:

```python
import requests
import pandas as pd

def prepare_batch_prediction_data(df):
    tweet_ids = [hash_tweet(text) for text in df['tweets']]
    texts = df['tweets'].tolist()
    return {
        "tweet_ids": tweet_ids,
        "texts": texts
    }

def predict_batch(df):
    response = requests.post('http://127.0.0.1:8000/predict', json=prepare_batch_prediction_data(df))
    return response.json()

# Example usage
test_data = pd.DataFrame({'tweets': ["Tweet 1", "Tweet 2", "Tweet 3", "Tweet 4"]})
batch_prediction = predict_batch(test_data)
print("Batch Prediction Results:", batch_prediction)
```

## Development [incomplete implementation]

### Running Tests

1. Navigate to the `tests` directory:

   ```sh
   cd my_twitter/tests
   ```

2. Run the tests:

   ```sh
   pytest
   ```

## Notes

- Ensure the model files and tokenizer are in the correct directories before running the FastAPI server.
- Modify the paths in `predict.py` and `preprocess.py` if the directory structure changes.

---
