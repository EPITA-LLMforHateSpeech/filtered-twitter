import streamlit as st
from user_management import UserManager

class AdminManager:
    def __init__(self):
        self.user_manager = UserManager()

    def admin_dashboard(self):
        st.write("Admin Dashboard")
        
