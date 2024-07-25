import json
import streamlit_authenticator as stauth
import os



    
class UserManager:
    def __init__(self, user_file='user.json'):
        self.user_file = user_file
        self.current_user_id = None  # This should be set when the user logs in
        self.users = self.load_users()

    def set_current_user(self, user_id):
        self.current_user_id = user_id

    def get_current_user_id(self):
        return self.current_user_id

    def load_users(self):
        # Assuming load_json_file is a custom function for reading JSON files
        users_data = self.load_json_file(self.user_file)
        if users_data is None:
            return {}  # Return an empty dictionary if no data
        return users_data

    
    # def load_users(self):
    #     # with open(self.user_file) as f:
    #     #     return json.load(f)

    #     # Block adjusted to fix load bugs
    #     users_data = load_json_file(self.user_file)
    #     if users_data is None:
    #         self.users = {}
    #     else:
    #         self.users = users_data

    def load_json_file(self, filename):
        # Get the directory of the current script
        directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(directory, filename)

        if not os.path.exists(file_path):
            print(f"{filename} not found in the directory.")
            return None

        with open(file_path, 'r') as file:
            return json.load(file)
    def save_users(self, users):
        # with open(self.user_file, 'w') as f:
        #     json.dump(users, f)

        # Save users to the specified file
        directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(directory, self.user_file)
        
        with open(file_path, 'w') as file:
            json.dump(self.users, file, indent=4)

    def add_user(self, username, password, name):
        hasher = stauth.Hasher([password])
        hashed_password = hasher.generate()[0]
        users = self.load_users()
        users['usernames'][username] = {"password": hashed_password, "name": name, "admin": False, "tweets": []}
        self.save_users(users)

    def delete_user(self, username):
        users = self.load_users()
        if username in users['usernames']:
            del users['usernames'][username]
            self.save_users(users)

class AdminManager(UserManager):
    def add_admin(self, username, password, name):
        hasher = stauth.Hasher([password])
        hashed_password = hasher.generate()[0]
        users = self.load_users()
        users['usernames'][username] = {"password": hashed_password, "name": name, "admin": True, "tweets": []}
        self.save_users(users)
    

    def remove_admin(self, username):
        users = self.load_users()
        if username in users['usernames']:
            users['usernames'][username]['admin'] = False
            self.save_users(users)
          
