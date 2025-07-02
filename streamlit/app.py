import streamlit as st
import json
import streamlit_authenticator as stauth
from interaction import InteractionManager
from profile_management import ProfileManager
from user_management import UserManager
from tweet_management import TweetManager
import admin_management
import os

# Load user data
users = {}
admins = {}


def load_json_file(filename):
    # Get the directory of the current script
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, filename)

    if not os.path.exists(file_path):
        print(f"{filename} not found in the directory.")
        return None

    with open(file_path, 'r') as file:
        return json.load(file)
    
users = load_json_file('user.json')
admins = load_json_file('admin.json')


# Combine user and admin data based on the structure
all_users = {}
if isinstance(users, dict):
    if 'usernames' in users:
        all_users.update(users['usernames'])
    else:
        print("No 'usernames' key found in users data.")

if isinstance(admins, dict):
    if 'usernames' in admins:
        all_users.update(admins['usernames'])
    else:
        print("No 'usernames' key found in admins data.")

# Check if the data combined successfully
if all_users:
    # print("All users data combined successfully.")
    pass
else:
    print("Failed to combine user and admin data.")


# Print combined data for verification
# print("Combined Users Data:", all_users)

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


    # interaction_manager = InteractionManager()  # Initialize the interaction manager

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

        user_manager = UserManager()  # Initialize UserManager
        user_manager.set_current_user(username)

        st.sidebar.title(f"Welcome {name}")
        authenticator.logout("Logout", "sidebar")

        # Determine user role
        is_admin = all_users.get(username, {}).get('admin', False)

        # menu = ["Home", "Profile", "Tweets", "Admin"]
        # Adjust menu options based on user role
        menu = []
        if not is_admin:
            menu = ["Home", "Profile", "Tweets"]
        else:
            menu = ["Admin"]

        # if all_users.get(username, {}).get('admin', False):
        #     menu.remove("Home")

    
        choice = st.sidebar.selectbox("Menu", menu)
        

        if choice == "Home":
            if not is_admin:
                st.subheader("Home")
                
                # Create a new tweet
                st.write("Create a new Tweet:")
                new_tweet = st.text_area("Tweet")
                if st.button("Post Tweet"):
                    if new_tweet.strip():  # Ensure the tweet is not empty
                        tweet_manager = TweetManager(user_manager)
                        tweet_manager.create_tweet(new_tweet)
                    else:
                        st.error("Tweet cannot be empty.")
                
                # Display existing tweets and interactions
                interaction_manager = InteractionManager(user_manager)
                interaction_manager.view_tweets()
            else:
                st.error('Only users have access to this page.')

        elif choice == "Profile":
            if not is_admin:
                st.subheader("Profile")

                profile_manager = ProfileManager(user_manager)
                profile_manager.display_profile(username)
            else:
                st.error('Only users have access to this page.')

        elif choice == "Tweets":
            if not is_admin:
                tweet_management = TweetManager(user_manager)
                st.subheader("Your Tweets")
                tweet_management.display_tweets()

            else:
                st.error('Only users have access to this page.')

        elif choice == "Admin":
            if is_admin:
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
