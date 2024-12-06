import json

class UserManager:
    def __init__(self, user_file='../../user.json'):
        self.user_file = user_file

    def load_users(self):
        with open(self.user_file) as f:
            return json.load(f)

    def save_users(self, users):
        with open(self.user_file, 'w') as f:
            json.dump(users, f)

    def add_user(self, username, password, name):
        users = self.load_users()
        users[username] = {"password": password, "name": name, "following": [], "followers": [], "tweets": []}
        self.save_users(users)

    def delete_user(self, username):
        users = self.load_users()
        if username in users:
            del users[username]
            self.save_users(users)

            
