import streamlit as st
import json
import streamlit_authenticator as stauth
import user_management
import tweet_management
import admin_management
from interaction import InteractionManager
from profile_management import ProfileManager
from user_management import UserManager
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
interaction_manager = InteractionManager()  # Initialize the interaction manager


# Initialize the authenticator
authenticator = stauth.Authenticate(
    credentials,
    "some_cookie_name",  # You can name this as you like
    "some_signature_key",  # A secret key to sign the cookie
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
        # Display tweets and interactions
        interaction_manager.view_tweets(username)

    elif choice == "Profile":
        st.subheader("Profile")
        user_manager = UserManager()  # Replace with your actual UserManager instance
        profile_manager = ProfileManager(user_manager)
 
    # Example profile display
        current_username = 'user1'  # Replace with dynamic username if needed
        profile_manager.display_profile(current_username)

    elif choice == "Tweets":
        st.subheader("Your Tweets")
        tweet_management.display_tweets(username)

    elif choice == "Admin":
        st.subheader("Admin")
        admin_management.admin_dashboard()

elif authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")