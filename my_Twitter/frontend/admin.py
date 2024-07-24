import streamlit as st
import requests

BASE_URL = "http://localhost:8000"

def fetch_all_tweets():
    response = requests.get(f"{BASE_URL}/fetch_tweets")
    return response.json()

def fetch_reported_tweets():
    response = requests.get(f"{BASE_URL}/reported_tweets")
    return response.json()

def fetch_safety_status_changes():
    response = requests.get(f"{BASE_URL}/safety_status_changes")
    return response.json()

def update_safety_status(tweet_id, new_safety_status, change_source):
    data = {
        "tweet_id": tweet_id,
        "new_safety_status": new_safety_status,
        "change_source": change_source
    }
    response = requests.post(f"{BASE_URL}/update_safety_status", json=data)
    return response.json()

# Function to fetch a tweet by ID
def fetch_tweet_by_id(tweet_id):
    response = requests.get(f"{BASE_URL}/fetch_tweet/{tweet_id}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Tweet not found")
        return None
    

def load_admin_page():
    st.header("Admin Panel")

    # Goes under All tweets ##########################################################
    # Fetch all tweets section
    st.subheader("Fetch All Tweets")
    if st.button("Fetch All Tweets"): # no buttons 
        all_tweets = fetch_all_tweets()
        for tweet in all_tweets:
            # Display username in small text
            st.markdown(f"<small>{tweet.get('user', 'Not available')} |  tweet id: {tweet.get('tweet_id', '')}</small>", unsafe_allow_html=True)

            # Display tweet content
            st.write(tweet.get('tweet', 'Not available'))

            # Display likes, retweets, and admin result in small text
            st.markdown(
                f"<small>Likes: {tweet.get('likes', 'Not available')} | Retweets: {tweet.get('retweets', 'Not available')} | Admin Result: {tweet.get('admin_result', 'Not available')}</small>",
                unsafe_allow_html=True
            )

            # Display model results in small text
            st.markdown(
                f"<small>Logreg Prob: {tweet.get('logreg_prob', 'Not available')} | Logreg Result: {tweet.get('logreg_result', 'Not available')} | CNN Prob: {tweet.get('cnn_prob', 'Not available')} | CNN Result: {tweet.get('cnn_result', 'Not available')}</small>",
                unsafe_allow_html=True
            )

            # Add a separator line
            st.write("---")

    ##################################################################
    # Goes under pending
    # Fetch reported tweets section
    st.subheader("Fetch Reported Tweets")
    if st.button("Fetch Reported Tweets"): # no buttons 
        reported_tweets = fetch_reported_tweets()
        for report in reported_tweets:
            tweet = fetch_tweet_by_id(report['tweet_id'])
            if tweet:
                # Display tweet details
                st.markdown(f"<small>{tweet.get('user_id', 'Not available')} \t\t |  tweet id: {report.get('tweet_id', '')}</small>", unsafe_allow_html=True)
                st.write(tweet.get('text', 'Not available'))
                st.markdown(
                    f"<small>Likes: {tweet.get('likes', 'Not available')} \t\t| Retweets: {tweet.get('retweets', 'Not available')} \t\t| Admin Result: {tweet.get('admin_result', 'Not available')}</small>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<small>Logreg Prob: {tweet.get('logreg_prob', 'Not available')} \t\t| Logreg Result: {tweet.get('logreg_result', 'Not available')} \t\t| CNN Prob: {tweet.get('cnn_prob', 'Not available')} \t\t| CNN Result: {tweet.get('cnn_result', 'Not available')}</small>",
                    unsafe_allow_html=True
                )
                st.write(f"Reported By: {report.get('user_id', 'Not available')}")
                st.write("---")



    # Update safety status section
    st.subheader("Update Safety Status")
    tweet_id = st.text_input("Tweet ID")
    new_safety_status = st.selectbox("New Safety Status", [0, 1])
    change_source = st.selectbox("Change Source", ["admin"])

    if st.button("Update Safety Status"):
        result = update_safety_status(tweet_id, new_safety_status, change_source)
        st.write(result)

###############################################################################################


    # Fetch safety status changes section
    st.subheader("Fetch Safety Status Changes")
    if st.button("Fetch Safety Status Changes"): 
        status_changes = fetch_safety_status_changes()
        for change in status_changes:
            st.write(f"Tweet ID: {change['tweet_id']}")
            st.write(f"New Safety Status: {change['new_safety_status']}")
            st.write(f"Change Source: {change['change_source']}")
            st.write("---")

########################### add another tab for statistics 
