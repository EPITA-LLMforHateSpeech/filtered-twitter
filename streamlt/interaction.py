import streamlit as st
from user_management import UserManager

class InteractionManager:
    def __init__(self):
        self.user_manager = UserManager()

    def like_tweet(self, username, tweet_id):
        # Load user data
        users = self.user_manager.load_users()
        
        # Iterate over all users to find the tweet
        for user in users['usernames'].values():
            for tweet in user['tweets']:
                if tweet['id'] == tweet_id:
                    tweet['like'] += 1
                    self.user_manager.save_users(users)
                    return
 
    def retweet(self, username, tweet_id):
        # Load user data
        users = self.user_manager.load_users()
 
        # Find the tweet to retweet
        tweet_to_retweet = None
        for user in users['usernames'].values():
            for tweet in user['tweets']:
                if tweet['id'] == tweet_id:
                    tweet_to_retweet = tweet
                    break
            if tweet_to_retweet:
                break
        
        if tweet_to_retweet:
            # Add the retweeted tweet to the current user's timeline
            users['usernames'][username]['tweets'].append(tweet_to_retweet)
            self.user_manager.save_users(users)
    
    def report_tweet(self, username, tweet_id):
        # Load user data
        users = self.user_manager.load_users()
 
        # Find and report the tweet
        for user in users['usernames'].values():
            for tweet in user['tweets']:
                if tweet['id'] == tweet_id:
                    tweet['safety_status'] = 'reported'
                    self.user_manager.save_users(users)
                    return
 

    def view_tweets(self, username):
        users = self.user_manager.load_users()
        print(users)
        # user_data = users['usernames'][username]
        for username, user_data in users['usernames'].items():
            for tweet in user_data['tweets']:
                st.write(f"{user_data['name']}: {tweet['text']} (Likes: {tweet['like']}, Retweets: {tweet['retweet']}, Status: {tweet['safety_status']})")
               