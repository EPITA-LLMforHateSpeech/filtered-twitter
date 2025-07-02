# Hate Speech Detection on Twitter using LLM

## Overview

This project aims to detect hate speech on Twitter using a machine learning pipeline involving linear regression and CNN models. The system is designed to facilitate user interactions, post tweets, and manage tweet safety status. The architecture leverages a Streamlit app for both user and admin interactions, with a backend powered by FastAPI and a database for storing and retrieving tweets and related metadata.

## System Architecture

![System Architecture](./final_architecture.png)

## Project Structure

```
filtered-twitter
    ├── backend
    │   ├── app
    │   │   ├── routes
    │   │   │   ├── __init__.py
    │   │   │   ├── admin.py
    │   │   │   ├── fetch_tweets.py
    │   │   │   ├── health.py
    │   │   │   ├── interact.py
    │   │   │   ├── predict.py
    │   │   │   ├── report_tweet.py
    │   │   │   ├── store_tweet.py
    │   │   │   ├── tweets_query.py
    │   │   ├── schemas
    │   │   │   ├── __init__.py
    │   │   │   ├── prediction.py
    │   │   │   ├── tweet.py
    │   │   ├── utils
    │   │   │   ├── __pycache__
    │   │   │   ├── __init__.py
    │   │   │   ├── db.py
    │   │   │   ├── prediction_utils.py
    │   │   │   ├── preprocess.py
    │   │   ├── __init__.py
    │   │   ├── main.py
    │   ├── database
    │   │   ├── __pycache__
    │   │   ├── db.py
    │   │   ├── models.py
    │   ├── models
    │   │   ├── cnn_model_regularization.keras
    │   │   ├── logistic_regression_model.pkl
    │   │   ├── tfidf_vectorizer.joblib
    │   │   ├── tokenizer.pickle
    │   ├── data
    │   │   ├── test.csv
    ├── streamlit
    │   ├── __pycache__
    │   ├── fastapi-backend
    │   ├── admin_management.py
    │   ├── admin.json
    │   ├── app.py
    │   ├── interaction.py
    │   ├── profile_management.py
    │   ├── tweet_management.py
    │   ├── user_management.py
    │   ├── user.json
    ├── filtered_tweets.db
    ├── requirements.txt
```

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/EPITA-LLMforHateSpeech/filtered-twitter.git
   cd filtered-twitter
   ```

2. **Create and activate a virtual environment:** [Optional]

   ```sh
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install the required packages:**

   ```sh
   pip install -r requirements.txt
   ```

4. Run the frontend:

   ```sh
   uvicorn backend.app.main:app --reload
   ```

5. Launch the webapp:
   From another terminal, run:

   ```sh
   streamlit run .\streamlit\app.py
   ```

### Components

1. **Streamlit App**

   - **User Page**
     - View other users' tweets
     - User profile management
     - Post tweets (after real-time hate speech detection passes)
     - View own tweets marked unsafe
   - **Admin Page**
     - View tweets in separate tabs (safe, pending admin input, unsafe)
     - View model results
     - Manually mark tweets as unsafe
     - Monitor users with a high amount of unsafe tweets

2. **FastAPI**

   - Handles prediction requests (real-time and batch)
   - Tracks prediction results and updates safety status
   - Logs user interactions
   - Manages database interactions

3. **Backend (Python)**

   - Implements the core logic for prediction and data management
   - Periodically checks the database for tweets requiring batch predictions
   - Updates tweet safety status based on model predictions or admin input

4. **Database Storage**
   - **tweets**: Stores complete tweet data, including predicted results
   - **stored_tweets**: Stores metadata of tweets allowed to be posted
   - **reported_tweets**: Stores information about reported tweets
   - **safety_status_changes**: Tracks changes to tweet safety status
   - **user_tweet_interactions**: Logs user interactions with tweets
   - **blocked_users**: Tracks users blocked by the admin

### User Interactions

- **Account Management**
  - Login with pre-authorized users
  - Session management using `streamlit-authenticator`
- **Post Tweets**
  - Create new tweets (allowed if real-time hate speech detection passes)
- **View Tweets**
  - Safe tweets are interactable
  - Unsafe tweets need a toggle to display content and are not interactable
- **Interact with Tweets**
  - Like, retweet, and report tweets
  - Admin can block user interactions
- **Retweet**
  - Similar to posting new tweets, goes through real-time detection

### Admin Interactions

- **User Authentication**
  - Managed with `streamlit-authenticator`
  - Admins stored in a JSON file, must be pre-authorized
- **Monitor Tweets and Users**
  - Mark tweets as unsafe/safe
  - Log frequent unsafe interactions
- **Dashboard**
  - View marked unsafe tweets vs. total tweets
  - View contributions of models/admin in marking tweets as unsafe

## Database Schema

### Tweets

- `tweet_id` (String, unique, indexed)
- `retweet_id` (String, nullable)
- `tweet` (Text, nullable=False)
- `user` (String, nullable=False)
- `likes` (Integer, default=0)
- `retweets` (Integer, default=0)
- `logreg_prob` (Float, nullable=True)
- `logreg_result` (Integer, nullable=True)
- `cnn_prob` (Float, nullable=True)
- `cnn_result` (Integer, nullable=True)
- `admin_result` (Integer, nullable=True)
- `created_at` (DateTime, default=current timestamp)

### Stored Tweets

- `id` (Integer, primary key, indexed)
- `tweet_id` (String, unique, indexed)
- `retweet_id` (String, nullable)
- `user_id` (String, nullable=False)
- `text` (Text, nullable=False)
- `likes` (Integer, default=0)
- `retweets` (Integer, default=0)
- `safety_status` (Integer, nullable=True)
- `created_at` (DateTime, default=current timestamp)

### Reported Tweets

- `id` (Integer, primary key, indexed)
- `tweet_id` (String, ForeignKey to 'tweets.tweet_id', nullable=False)
- `user_id` (String, nullable=False)
- `reported_at` (DateTime, default=current timestamp)

### Safety Status Changes

- `id` (Integer, primary key, indexed)
- `tweet_id` (String, ForeignKey to 'tweets.tweet_id', nullable=False)
- `new_safety_status` (Integer, nullable=False)
- `change_source` (String, nullable=False)
- `changed_at` (DateTime, default=current timestamp)

### User Tweet Interactions

- `id` (Integer, primary key, indexed)
- `user_id` (String, nullable=False)
- `tweet_id` (String, nullable=False)
- `interaction_type` (String, nullable=False)
- `created_at` (DateTime, default=current timestamp)

### Blocked Users

- `user_id` (String, primary key, indexed)

## API Endpoints

1. **User Actions**
   - `/submit_tweet`: Submit new tweets for prediction
   - `/like_tweet`: Like a tweet
   - `/retweet`: Retweet a post
   - `/report_tweet`: Report a tweet as unsafe
2. **Admin Actions**
   - `/fetch_tweets`: Fetch all stored tweets
   - `/reported_tweets`: Fetch reported tweets
   - `/safety_status_changes`: Fetch tweets with updated safety status
   - `/update_safety_status`: Update safety status of a tweet
3. **Batch Predictions**
   - Batch predictions run every 30 seconds (for debugging)

## Simulation

- Posts tweets for 8 users, 50 tweets over an hour
- Random intervals between 1-3 tweets per user
- Simulation graph displays the top 3 users with most hate speech tweets

## Getting Started

1. **Setup Streamlit App**
   - Define user and admin roles
   - Load respective pages based on role
2. **Configure FastAPI Backend**
   - Ensure all endpoints are properly defined
   - Implement prediction logic and database interaction
3. **Database Initialization**
   - Setup necessary tables and relationships
   - Populate with initial data as needed

## Conclusion

This project provides a comprehensive system for detecting and managing hate speech on Twitter, incorporating real-time and batch processing, user and admin interfaces, and robust database management.

---
