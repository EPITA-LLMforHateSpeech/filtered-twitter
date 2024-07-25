import streamlit as st
from user_management import UserManager
import requests
from datetime import datetime, timezone


class InteractionManager:
    BASE_URL = "http://localhost:8000"


    def __init__(self, user_manager):
        self.user_manager = user_manager

    def like_tweet(self, tweet_id):
        url = f"{self.BASE_URL}/like_tweet"
        payload = {"tweet_id": tweet_id}
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            st.success("Tweet liked successfully.")
        else:
            st.error(f"Failed to like tweet: {response.status_code}")
            st.error(f"Response: {response.json()}")
 
    def retweet_tweet(self, tweet_id):
        url = f"{self.BASE_URL}/retweet_tweet"
        payload = {"tweet_id": tweet_id}
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            st.success("Tweet retweeted successfully.")
        else:
            st.error(f"Failed to retweet tweet: {response.status_code}")
            st.error(f"Response: {response.json()}")
    

    def report_tweet(self, tweet_id, user_id):
        report_data = {
            "tweet_id": tweet_id,
            "user_id": user_id,
            "safety_status": 1,  # Example: 1 for hate speech
            "reported_at": datetime.now(timezone.utc).isoformat()
        }
        url = f"{self.BASE_URL}/report_tweet"
        response = requests.post(url, json=report_data)
        
        if response.status_code == 200:
            st.success("Report submitted successfully.")
        else:
            st.error(f"Failed to submit report: {response.status_code}")
            st.error(f"Response: {response.json()}")
 

    def view_tweets(self):
        st.write("### All Tweets")
        
        # Initialize session state if it does not exist
        if 'show_blocked' not in st.session_state:
            st.session_state.show_blocked = False

        # Button to toggle blocked tweet display
        if st.button("Toggle Blocked Tweets"):
            st.session_state.show_blocked = not st.session_state.show_blocked
            st.experimental_rerun()  # Refresh the page to update tweet visibility
        
        with st.spinner("Loading tweets..."):
            all_tweets = self.fetch_user_view_tweets()
        
        if not all_tweets:
            st.error("Failed to fetch tweets or no tweets found.")
            return
        
        i = 0
        for tweet in all_tweets:
            # Determine if the tweet should be blocked based on safety_status
            is_blocked = tweet.get('safety_status') == 1
            
            # Display user ID and tweet ID, add [BLOCKED] if necessary
            user_display = f"{tweet.get('user_id', 'Not available')} | Tweet ID: {tweet.get('tweet_id', '')}"
            if is_blocked:
                if st.session_state.show_blocked:
                    user_display += " <span style='color: #FF6347;'> [BLOCKED]</span>"
                else:
                    user_display += " <span style='color: #FF6347;'> [BLOCKED] - <small>Click 'Toggle Blocked Tweets' to view</small></span>"
            st.markdown(f"<small>{user_display}</small>", unsafe_allow_html=True)

            # Display tweet content if not blocked or if blocked and the toggle is on
            if not is_blocked or st.session_state.show_blocked:
                st.write(tweet.get('text', 'Not available'))

                # Display likes and retweets in small text
                st.markdown(
                    f"<small>Likes: {tweet.get('likes', 'Not available')} | Retweets: {tweet.get('retweets', 'Not available')}</small>",
                    unsafe_allow_html=True
                )

                # Display action buttons for tweets not blocked by safety_status
                if not is_blocked:
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col1:
                        if st.button('Like', key=f'like_{tweet["tweet_id"] + str(i)}'):
                            self.like_tweet(tweet["tweet_id"])
                    
                    with col2:
                        if st.button('Retweet', key=f'retweet_{tweet["tweet_id"] + str(i)}'):
                            self.retweet_tweet(tweet["tweet_id"])
                    
                    with col3:
                        if st.button('Report', key=f'report_{tweet["tweet_id"] + str(i)}'):
                            user_id = self.user_manager.get_current_user_id() 
                            if user_id:
                                self.report_tweet(tweet["tweet_id"], user_id)  # Use the current user's ID for reporting
                            else: 
                                st.error('User not logged in.')
                st.write("---")

            i += 1


    def fetch_user_view_tweets(self):
        url = f"{self.BASE_URL}/display_tweets"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch tweets: {response.status_code}")
            st.error(f"Response: {response.json()}")
            return None