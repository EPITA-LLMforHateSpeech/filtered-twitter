import streamlit as st
from user_management import UserManager
 
class TweetManager:
    def __init__(self):
        self.user_manager = UserManager()
 
    def create_tweet(self, username, tweet_text):
        users = self.user_manager.load_users()
        tweet_id = max([tweet["id"] for user in users['usernames'].values() for tweet in user["tweets"]], default=0) + 1
        users['usernames'][username]["tweets"].append({"id": tweet_id, "text": tweet_text, "like": 0, "retweet": 0, "safety_status": "pending"})
        self.user_manager.save_users(users)
 
    def delete_tweet(self, username, tweet_id):
        users = self.user_manager.load_users()
        users['usernames'][username]["tweets"] = [tweet for tweet in users['usernames'][username]["tweets"] if tweet["id"] != tweet_id]
        self.user_manager.save_users(users)
 
    def update_tweet(self, username, tweet_id, new_text):
        users = self.user_manager.load_users()
        for tweet in users['usernames'][username]["tweets"]:
            if tweet["id"] == tweet_id:
                tweet["text"] = new_text
                tweet["safety_status"] = "pending"
                self.user_manager.save_users(users)
                break
 
    def display_tweets(self, username):
        users = self.user_manager.load_users()
        for user, user_data in users['usernames'].items():
            st.write(f"**{user_data['name']} ({user}):**")
            for tweet in user_data["tweets"]:
                st.write(f"{tweet['text']}") 
 
    