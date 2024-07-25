import streamlit as st
import json
import streamlit_authenticator as stauth
from interaction import InteractionManager
from profile_management import ProfileManager
from user_management import UserManager
import tweet_management
import admin_management
import os

# Load user data
users = {}
admins = {}

# try:
#     with open('user.json') as f:
#         users = json.load(f)
# except json.JSONDecodeError as e:
#     st.error(f"Error reading user JSON file: {e}")
# except FileNotFoundError as e:
#     st.error(f"User JSON file not found: {e}")
# except Exception as e:
#     st.error(f"An unexpected error occurred: {e}")

# try:
#     with open('admin.json') as f:
#         admins = json.load(f)
# except json.JSONDecodeError as e:
#     st.error(f"Error reading admin JSON file: {e}")
# except FileNotFoundError as e:
#     st.error(f"Admin JSON file not found: {e}")
# except Exception as e:
#     st.error(f"An unexpected error occurred: {e}")

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
    print("All users data combined successfully.")
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
                interaction_manager.view_tweets(username)
            else:
                st.error('Only users have access to this page.')
        elif choice == "Profile":
            if not is_admin:
                st.subheader("Profile")
                user_manager = UserManager()  # Replace with your actual UserManager instance
                profile_manager = ProfileManager(user_manager)
                profile_manager.display_profile(username)
            else:
                st.error('Only users have access to this page.')

        elif choice == "Tweets":
            if not is_admin:
                st.subheader("Your Tweets")
                tweet_management.display_tweets(username)
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
