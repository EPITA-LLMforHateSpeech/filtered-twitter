import streamlit as st
from user_management import UserManager

class ProfileManager:
    def __init__(self, user_manager):
        self.user_manager = user_manager
 
    def update_profile(self, username, new_name):
        # Load user data
        users = self.user_manager.load_users()
        # Update the profile name
        if username in users['usernames']:
            users['usernames'][username]['name'] = new_name
            self.user_manager.save_users(users)
            return True
        return False
 
    def display_profile(self, username):
        # Load user data
        users = self.user_manager.load_users()
        if username in users['usernames']:
            user_data = users['usernames'][username]
            # Display the profile
            st.write(f"**Username:** {username}")
            st.write(f"**Name:** {user_data['name']}")
            st.write(f"**Email:** {user_data['email']}")
 
            # Update profile section
            new_name = st.text_input('New Name', value=user_data['name'])
            if st.button('Change Name'):
                if self.update_profile(username, new_name):
                    st.success('Name updated successfully')
                else:
                    st.error('Failed to update profile')
 
# # Example usage
# if __name__ == "__main__":
#     # Instantiate UserManager and ProfileManager
#     user_manager = UserManager()  # Replace with your actual UserManager instance
#     profile_manager = ProfileManager(user_manager)
 
#     # Example profile display
#     current_username = 'user1'  # Replace with dynamic username if needed
#     profile_manager.display_profile(current_username)
