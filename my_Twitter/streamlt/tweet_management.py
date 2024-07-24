import streamlit as st
from user_management import UserManager

class TweetManager:
    def __init__(self):
        self.user_manager = UserManager()

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

    def display_tweets(self, username):
        users = self.user_manager.load_users()
        if username in users:
            st.write(f"Tweets by {username}:")
            for tweet in users[username]["tweets"]:
                st.write(f"{tweet['text']} (Likes: {tweet['likes']}, Retweets: {tweet['retweets']}, Status: {tweet['safety_status']})")
                new_text = st.text_input(f'New Text for Tweet {tweet["id"]}')
                if st.button(f'Update Tweet {tweet["id"]}'):
                    self.update_tweet(username, tweet["id"], new_text)
                    st.success('Tweet updated successfully')
                if st.button(f'Delete Tweet {tweet["id"]}'):
                    self.delete_tweet(username, tweet["id"])
                    st.success('Tweet deleted successfully')
