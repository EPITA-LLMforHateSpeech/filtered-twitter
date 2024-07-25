import streamlit as st
from user_management import UserManager
import requests
class TweetManager:

    BASE_URL = "http://localhost:8000"


    def __init__(self, user_manager):
        self.user_manager = user_manager

    def create_tweet(self, username, tweet_text):
        users = self.user_manager.load_users()
        tweet_id = len(users[username]["tweets"])
        users[username]["tweets"].append({"id": tweet_id, "text": tweet_text, "likes": 0, "retweets": 0, "safety_status": "pending"})
        self.user_manager.save_users(users)

    def delete_tweet(self, username, tweet_id):
        users = self.user_manager.load_users()
        users[username]["tweets"] = [tweet for tweet in users[username]["tweets"] if tweet["id"] != tweet_id]
        self.user_manager.save_users(users)

    def update_tweet(self, username, tweet_id, new_text):
        users = self.user_manager.load_users()
        for tweet in users[username]["tweets"]:
            if tweet["id"] == tweet_id:
                tweet["text"] = new_text
                tweet["safety_status"] = "pending"
                self.user_manager.save_users(users)
                break

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