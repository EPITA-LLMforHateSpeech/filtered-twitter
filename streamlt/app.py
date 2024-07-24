import streamlit as st
import json
import streamlit_authenticator as stauth
from user_management import UserManager
from tweet_management import TweetManager
from profile_management import ProfileManager

# Load user data
with open('user.json') as f:
    users = json.load(f)
 
# Extract user data for authenticator
usernames = list(users['usernames'].keys())
names = [users['usernames'][user]['name'] for user in usernames]
hashed_passwords = [users['usernames'][user]['password'] for user in usernames]
 
# Prepare credentials dictionary
credentials = {
    'usernames': {
        username: {
            'name': users['usernames'][username]['name'],
            'password': users['usernames'][username]['password']
        }
        for username in usernames
    }
}
 
# Initialize managers
interaction_manager = TweetManager()
tweet_manager = TweetManager()
user_manager = UserManager()
profile_manager = ProfileManager(user_manager)


# Initialize the authenticator
authenticator = stauth.Authenticate(
    credentials,
    "some_cookie_name",
    "some_signature_key",
)
 
# Authentication
name, authentication_status, username = authenticator.login()
 
if authentication_status:
    st.sidebar.title(f"Welcome {name}")
    authenticator.logout("Logout", "sidebar")
 
    menu = ["Home", "Profile", "Tweets", "Admin"]
    choice = st.sidebar.selectbox("Menu", menu)
 
    if choice == "Home":
        st.subheader("Home")
        st.write("Create a new Tweet:")
        new_tweet = st.text_area("Tweet")
        if st.button("Post Tweet"):
            tweet_manager.create_tweet(username, new_tweet)
            st.success("Tweet created successfully")
        # Display tweets and interactions
        tweet_manager.display_tweets(username)
 
    elif choice == "Profile":
        st.subheader("Profile")
        profile_manager.display_profile(username)
 
    elif choice == "Tweets":
        st.subheader("Your Tweets")
        st.write("Create a new Tweet:")
        new_tweet = st.text_area("Tweet")
        if st.button("Post Tweet"):
            tweet_manager.create_tweet(username, new_tweet)
            st.success("Tweet created successfully")
        tweet_manager.display_tweets(username)
 
    # elif choice == "Admin":
    #     st.subheader("Admin")
    #     admin_management.admin_page(username)

elif authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")


###########################################################################################################################

