import json
import streamlit_authenticator as stauth

class UserManager:
    def __init__(self, user_file='user.json'):
        self.user_file = user_file

    def load_users(self):
        with open(self.user_file) as f:
            return json.load(f)

    def save_users(self, users):
        with open(self.user_file, 'w') as f:
            json.dump(users, f)

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
          
