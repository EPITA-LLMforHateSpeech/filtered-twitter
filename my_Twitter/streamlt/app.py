import streamlit as st
import json
import streamlit_authenticator as stauth
from interaction import InteractionManager
from profile_management import ProfileManager
from user_management import UserManager
import tweet_management
import admin_management

# Load user data
users = {}
admins = {}

try:
    with open('user.json') as f:
        users = json.load(f)
except json.JSONDecodeError as e:
    st.error(f"Error reading user JSON file: {e}")
except FileNotFoundError as e:
    st.error(f"User JSON file not found: {e}")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")

try:
    with open('admin.json') as f:
        admins = json.load(f)
except json.JSONDecodeError as e:
    st.error(f"Error reading admin JSON file: {e}")
except FileNotFoundError as e:
    st.error(f"Admin JSON file not found: {e}")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")

# Combine user and admin data
all_users = {**users.get('usernames', {}), **admins.get('usernames', {})}




# Check if the data loaded successfully
if all_users:
    usernames = list(all_users.keys())
    names = [all_users[user]['name'] for user in usernames]
    hashed_passwords = [all_users[user]['password'] for user in usernames]

    # Prepare credentials dictionary
    credentials = {
        'usernames': {
            username: {
                'name': all_users[username]['name'],
                'password': all_users[username]['password']
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
        cookie_expiry_days=30
    )

    # Authentication
    name, authentication_status, username = authenticator.login()

    if authentication_status:
        st.sidebar.title(f"Welcome {name}")
        authenticator.logout("Logout", "sidebar")

        menu = ["Home", "Profile", "Tweets", "Admin"]
        if all_users.get(username, {}).get('admin', False):
            menu.remove("Home")

    
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Home":
            st.subheader("Home")
            interaction_manager.view_tweets(username)

        elif choice == "Profile":
            st.subheader("Profile")
            user_manager = UserManager()  # Replace with your actual UserManager instance
            profile_manager = ProfileManager(user_manager)
            profile_manager.display_profile(username)

        elif choice == "Tweets":
            st.subheader("Your Tweets")
            tweet_management.display_tweets(username)

        elif choice == "Admin":
            if all_users.get(username, {}).get('admin', False):
                st.subheader("Admin")
                admin_management.admin_dashboard()
            else:
                st.error("You are not authorized to view this page.")

    elif authentication_status is False:
        st.error("Username/password is incorrect")
    elif authentication_status is None:
        st.warning("Please enter your username and password")
else:
    st.error("Failed to load user or admin data.")
    st.stop()
