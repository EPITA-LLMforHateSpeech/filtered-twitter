import streamlit as st
from user_management import AdminManager
import requests
import pandas as pd



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
    

def fetch_risky_tweets():
    response = requests.get(f"{BASE_URL}/tweets/risky")
    if response.status_code == 200:
        return response.json()
    else:
        return None
    

def fetch_cnn_unsafe_tweets():
    response = requests.get(f"{BASE_URL}/tweets/unsafe/cnn")
    if response.status_code == 200:
        return response.json()
    else:
        return None

def fetch_admin_unsafe_tweets():
    response = requests.get(f"{BASE_URL}/tweets/unsafe/admin")
    if response.status_code == 200:
        return response.json()
    else:
        return None
    


def admin_dashboard():
    admin_manager = AdminManager()

    st.write("## Admin Dashboard")

    # Tabs for viewing different categories of tweets
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["All Tweets", "Pending Tweets", "Unsafe Tweets", "Statistics", "User management"])

    with tab1:
        st.write("### All Tweets")
        with st.spinner("Loading tweets..."):
            all_tweets = fetch_all_tweets()  # Call your function to fetch tweets

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

    with tab2:
        st.write("### Pending Tweets")
        pending_tabs = st.tabs(["User Reports", "Risky Tweets"])
        with pending_tabs[0]:
            st.write("Here are tweets reported by users and awaiting admin result.")
            with st.spinner("Loading tweets..."):
                reported_tweets = fetch_reported_tweets()
                for report in reported_tweets:
                    tweet = fetch_tweet_by_id(report['tweet_id'])
                    if tweet:
                        # Display tweet details
                        st.markdown(f"<small>{tweet.get('user_id', 'Not available')} \t\t |  tweet id: {report.get('tweet_id', '')}</small>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: #FF6347;'>{tweet.get('text', 'Not available')}</p>", unsafe_allow_html=True)
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

        with pending_tabs[1]:
            st.write("Here are tweets that had high probabilities (higher than 30%) with the cnn model but were not reported hate speech.")
            with st.spinner("Loading tweets..."):
                risky_tweets = fetch_risky_tweets()
                if risky_tweets:
                    for tweet in risky_tweets:
                        st.markdown(f"<small>{tweet.get('user', 'Not available')} | tweet id: {tweet.get('tweet_id', '')}</small>", unsafe_allow_html=True)
                        st.write(f"<span style='color: #FF6347;'>{tweet.get('tweet', 'Not available')}</span>", unsafe_allow_html=True)
                        st.markdown(f"<small>Likes: {tweet.get('likes', 'Not available')} | Retweets: {tweet.get('retweets', 'Not available')} | Admin Result: {tweet.get('admin_result', 'Not available')}</small>", unsafe_allow_html=True)
                        st.markdown(f"<small>Logreg Prob: {tweet.get('logreg_prob', 'Not available')} | Logreg Result: {tweet.get('logreg_result', 'Not available')} | CNN Prob: {tweet.get('cnn_prob', 'Not available')} | CNN Result: {tweet.get('cnn_result', 'Not available')}</small>", unsafe_allow_html=True)
                        st.write("---")
                else:
                    st.write("No risky tweets found.")

    with tab3:
        st.write("### Unsafe Tweets")
        st.write("Unsafe tweets will be displayed here.")
        unsafe_tabs = st.tabs(["CNN Unsafe Tweets", "Admin Unsafe Tweets"])
        with unsafe_tabs[0]:
            st.write("### CNN Unsafe Tweets")
            cnn_unsafe_tweets = fetch_cnn_unsafe_tweets()
            if cnn_unsafe_tweets:
                for tweet in cnn_unsafe_tweets:
                    st.markdown(f"<small>{tweet.get('user', 'Not available')} | tweet id: {tweet.get('tweet_id', '')}</small>", unsafe_allow_html=True)
                    st.write(f"<span style='color:#FF6347;'>{tweet.get('tweet', 'Not available')}</span>", unsafe_allow_html=True)
                    st.markdown(f"<small>Likes: {tweet.get('likes', 'Not available')} | Retweets: {tweet.get('retweets', 'Not available')} | Admin Result: {tweet.get('admin_result', 'Not available')}</small>", unsafe_allow_html=True)
                    st.markdown(f"<small>Logreg Prob: {tweet.get('logreg_prob', 'Not available')} | Logreg Result: {tweet.get('logreg_result', 'Not available')} | CNN Prob: {tweet.get('cnn_prob', 'Not available')} | CNN Result: {tweet.get('cnn_result', 'Not available')}</small>", unsafe_allow_html=True)
                    st.write("---")
            else:
                st.write("No CNN unsafe tweets found.")

        with unsafe_tabs[1]:
            st.write("### Admin Unsafe Tweets")
            admin_unsafe_tweets = fetch_admin_unsafe_tweets()
            if admin_unsafe_tweets:
                for tweet in admin_unsafe_tweets:
                    st.markdown(f"<small>{tweet.get('user', 'Not available')} | tweet id: {tweet.get('tweet_id', '')}</small>", unsafe_allow_html=True)
                    st.write(f"<span style='color:#FF6347;'>{tweet.get('tweet', 'Not available')}</span>", unsafe_allow_html=True)
                    st.markdown(f"<small>Likes: {tweet.get('likes', 'Not available')} | Retweets: {tweet.get('retweets', 'Not available')} | Admin Result: {tweet.get('admin_result', 'Not available')}</small>", unsafe_allow_html=True)
                    st.markdown(f"<small>Logreg Prob: {tweet.get('logreg_prob', 'Not available')} | Logreg Result: {tweet.get('logreg_result', 'Not available')} | CNN Prob: {tweet.get('cnn_prob', 'Not available')} | CNN Result: {tweet.get('cnn_result', 'Not available')}</small>", unsafe_allow_html=True)
                    st.write("---")
            else:
                st.write("No admin unsafe tweets found.")
    with tab4:
        st.write("### Statistics Tweets")
        st.write("Statistics will be displayed here.")

    with tab5:
        # Admin functionalities section
        st.write("## Admin Functions")

        # Add User
        st.write("### Add User")
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password")
        new_name = st.text_input("Name")
        if st.button("Add User"):
            if new_username and new_password and new_name:
                admin_manager.add_user(new_username, new_password, new_name)
                st.success(f"User {new_username} added successfully.")
            else:
                st.error("Please fill in all fields to add a user.")

        # Add Admin
        st.write("### Add Admin")
        new_admin_username = st.text_input("Admin Username")
        new_admin_password = st.text_input("Admin Password", type="password")
        new_admin_name = st.text_input("Admin Name")
        if st.button("Add Admin"):
            if new_admin_username and new_admin_password and new_admin_name:
                admin_manager.add_admin(new_admin_username, new_admin_password, new_admin_name)
                st.success(f"Admin {new_admin_username} added successfully.")
            else:
                st.error("Please fill in all fields to add an admin.")

        # Delete User
        st.write("### Delete User")
        del_username = st.text_input("Username to delete")
        if st.button("Delete User"):
            if del_username:
                admin_manager.delete_user(del_username)
                st.success(f"User {del_username} deleted successfully.")
            else:
                st.error("Please provide a username to delete.")
