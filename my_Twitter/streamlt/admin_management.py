import streamlit as st
from user_management import AdminManager

def admin_dashboard():
    admin_manager = AdminManager()

    st.write("## Admin Dashboard")

    # Tabs for viewing different categories of tweets
    tab1, tab2, tab3, tab4 = st.tabs(["All Tweets", "Pending Tweets", "Unsafe Tweets", "Statistics"])

    with tab1:
        st.write("### All Tweets")
        st.write("All tweets will be displayed here.")

    with tab2:
        st.write("### Pending Tweets")
        st.write("Pending tweets will be displayed here.")

    with tab3:
        st.write("### Unsafe Tweets")
        st.write("Unsafe tweets will be displayed here.")

    with tab4:
        st.write("### Statistics Tweets")
        st.write("Statistics will be displayed here.")

    # Admin functionalities section
    st.write("## Admin Functions")

    # Add User
    st.write("### Add User")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    new_name = st.text_input("Name")
    if st.button("Add User"):
        if new_username and new_password and new_name:
            admin_manager.add_user(new_username, new_password, new_name)
            st.success(f"User {new_username} added successfully.")
        else:
            st.error("Please fill in all fields to add a user.")

    # Add Admin
    st.write("### Add Admin")
    new_admin_username = st.text_input("Admin Username")
    new_admin_password = st.text_input("Admin Password", type="password")
    new_admin_name = st.text_input("Admin Name")
    if st.button("Add Admin"):
        if new_admin_username and new_admin_password and new_admin_name:
            admin_manager.add_admin(new_admin_username, new_admin_password, new_admin_name)
            st.success(f"Admin {new_admin_username} added successfully.")
        else:
            st.error("Please fill in all fields to add an admin.")

    # Delete User
    st.write("### Delete User")
    del_username = st.text_input("Username to delete")
    if st.button("Delete User"):
        if del_username:
            admin_manager.delete_user(del_username)
            st.success(f"User {del_username} deleted successfully.")
        else:
            st.error("Please provide a username to delete.")
