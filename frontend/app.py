import streamlit as st
import admin
import user

st.title("Welcome to the Hate Speech Detection System")

# Selection buttons
if st.button("Admin"):
    st.session_state["role"] = "admin"

if st.button("User"):
    st.session_state["role"] = "user"

# Load the appropriate interface based on the selected role
if "role" in st.session_state:
    if st.session_state["role"] == "admin":
        admin.load_admin_page()
    elif st.session_state["role"] == "user":
        user.load_user_page()
else:
    st.write("Please select your role to proceed.")
