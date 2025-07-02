import streamlit as st
from user_management import UserManager
import requests
from datetime import datetime, timezone


class TweetManager:

    BASE_URL = "http://localhost:8000"


    def __init__(self, user_manager):
        self.user_manager = user_manager

    def post_tweet_for_prediction(self, tweet, user):
        response = requests.post(f'{self.BASE_URL}/predict', json={"text": tweet, "user": user})
        return response.json()

    def store_posted_tweet(self, tweet_id, retweet_id, user_id, text, likes, retweets, safety_status, created_at):
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
        response = requests.post(f'{self.BASE_URL}/store_tweet', json=data)
        return response.json()
    
    def create_tweet(self, text):
        user_id = self.user_manager.get_current_user_id()
        if not user_id:
            raise ValueError("User ID is required to create a tweet.")
        
        # Post tweet for prediction
        prediction = self.post_tweet_for_prediction(text, user_id)
        print("Prediction Result:", prediction)

        # Check if the tweet is flagged as hate speech
        if prediction.get("logreg_result") == 0:
            created_at = datetime.now(timezone.utc).isoformat()  # Convert datetime to ISO format string

            # Store the posted tweet
            store_response = self.store_posted_tweet(
                tweet_id=prediction.get("tweet_id"),
                retweet_id=None,
                user_id=user_id,
                text=prediction.get("tweet"),
                likes=prediction.get("likes"),
                retweets=prediction.get("retweets"),
                safety_status=None,  # Initial safety status is None
                created_at=created_at
            )
            print("Store Tweet Response:", store_response)
            return {"success": f"Tweet passed hate speech check, stored under tweet id {store_response.get('tweet_id')}"}
        else:
            st.error("Tweet is flagged as hate speech and cannot be posted.")
            return {"error": "Tweet is flagged as hate speech and cannot be posted."}

    def delete_tweet(self, tweet_id):
        pass

    def update_tweet(self, tweet_id, new_text):
        pass

    def display_tweets(self):
        user_id = self.user_manager.get_current_user_id()  # Retrieve the current user ID

        if not user_id:
            st.error("User ID not found.")
            return
        
        st.write(f"Tweets by {user_id}:")

        # Fetch tweets for the current user
        tweets = self.fetch_tweets_by_user(user_id)

        if not tweets:
            st.error("Failed to fetch tweets or no tweets found.")
            return

        for tweet in tweets:
            st.write(f"{tweet['text']} (Likes: {tweet['likes']}, Retweets: {tweet['retweets']}, Status: {tweet['safety_status']})")
            
            new_text = st.text_input(f'New Text for Tweet {tweet["tweet_id"]}', value=tweet['text'])
            col1, col2 = st.columns([1, 1])
            
            with col1:
                if st.button(f'Update Tweet', key=f'update_{tweet["tweet_id"]}'):
                    self.update_tweet(user_id, tweet["tweet_id"], new_text)
                    st.success('Tweet updated successfully')
            
            with col2:
                if st.button(f'Delete Tweet', key=f'delete_{tweet["tweet_id"]}'):
                    self.delete_tweet(user_id, tweet["tweet_id"])
                    st.success('Tweet deleted successfully')
        
        st.write("---")


    def fetch_tweets_by_user(self, user_id):
        url = f"{self.BASE_URL}/fetch_tweets_by_user/{user_id}"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch tweets: {response.status_code}")
            st.error(f"Response: {response.json()}")
            return None

    def update_tweet(self, user_id, tweet_id, new_text):
        # Implement the update tweet functionality
        pass

    def delete_tweet(self, user_id, tweet_id):
        # Implement the delete tweet functionality
        pass