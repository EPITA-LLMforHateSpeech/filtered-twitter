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
                st.write(f"{tweet['text']}(Likes: {tweet['like']}, Retweets: {tweet['retweet']}, Status: {tweet['safety_status']})")
                if st.button(f'Like Tweet {tweet["id"]}', key=f'like_{tweet["id"]}'):
                    self.like_tweet(username, tweet["id"])
                    st.success('Tweet liked successfully')
                if st.button(f'Retweet {tweet["id"]}', key=f'retweet_{tweet["id"]}'):
                    self.retweet(username, tweet["id"])
                    st.success('Retweeted successfully')
                if st.button(f'Report Tweet {tweet["id"]}', key=f'report_{tweet["id"]}'):
                    self.report_tweet(username, tweet["id"])
                    st.success('Tweet reported successfully')
                if st.button(f'Delete Tweet {tweet["id"]}', key=f'delete_{tweet["id"]}'):
                    self.delete_tweet(user, tweet["id"])
                    st.success('Tweet deleted successfully')
                if st.button(f'Update Tweet {tweet["id"]}', key=f'update_{tweet["id"]}'):
                    self.show_update_field(username, tweet["id"], tweet['text'])
    
    def show_update_field(self, username, tweet_id, current_text):
        new_text = st.text_area(f'Update Tweet {tweet_id}', value=current_text, key=f'new_text_{tweet_id}')
        if st.button(f'Submit Update {tweet_id}', key=f'submit_update_{tweet_id}'):
            self.update_tweet(username, tweet_id, new_text)
            st.success('Tweet updated successfully')
 
    def like_tweet(self, username, tweet_id):
        users = self.user_manager.load_users()
        for user in users['usernames'].values():
            for tweet in user["tweets"]:
                if tweet["id"] == tweet_id:
                    tweet["like"] += 1
                    self.user_manager.save_users(users)
                    return
 
    def retweet(self, username, tweet_id):
        users = self.user_manager.load_users()
        tweet_to_retweet = None
        for user in users['usernames'].values():
            for tweet in user["tweets"]:
                if tweet["id"] == tweet_id:
                    tweet_to_retweet = tweet
                    break
            if tweet_to_retweet:
                break
 
        if tweet_to_retweet:
            users['usernames'][username]["tweets"].append(tweet_to_retweet)
            self.user_manager.save_users(users)
 
    def report_tweet(self, username, tweet_id):
        users = self.user_manager.load_users()
        for user in users['usernames'].values():
            for tweet in user["tweets"]:
                if tweet["id"] == tweet_id:
                    tweet["safety_status"] = "reported"
                    self.user_manager.save_users(users)
                    return
 
    