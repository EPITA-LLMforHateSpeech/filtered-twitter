import streamlit as st
from user_management import AdminManager
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
from io import BytesIO


BASE_URL = "http://localhost:8000"


def fetch_all_tweets():
    response = requests.get(f"{BASE_URL}/fetch_tweets")
    return response.json()

def fetch_reported_tweets():
    response = requests.get(f"{BASE_URL}/reported_tweets")
    return response.json()

def fetch_safety_status_changes():
    response = requests.get(f"{BASE_URL}/safety_status_changes")
    return response.json()

def update_safety_status(tweet_id, new_safety_status, change_source):
    data = {
        "tweet_id": tweet_id,
        "new_safety_status": new_safety_status,
        "change_source": change_source
    }
    response = requests.post(f"{BASE_URL}/update_safety_status", json=data)
    return response.json()

# Function to fetch a tweet by ID
def fetch_tweet_by_id(tweet_id):
    response = requests.get(f"{BASE_URL}/fetch_tweet/{tweet_id}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Tweet not found")
        return None
    

def fetch_risky_tweets():
    response = requests.get(f"{BASE_URL}/tweets/risky")
    if response.status_code == 200:
        return response.json()
    else:
        return None
    

def fetch_cnn_unsafe_tweets():
    response = requests.get(f"{BASE_URL}/tweets/unsafe/cnn")
    if response.status_code == 200:
        return response.json()
    else:
        return None

def fetch_admin_unsafe_tweets():
    response = requests.get(f"{BASE_URL}/tweets/unsafe/admin")
    if response.status_code == 200:
        return response.json()
    else:
        return None
    

def admin_dashboard():
    admin_manager = AdminManager()

    st.write("## Admin Dashboard")

    # Tabs for viewing different categories of tweets
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["All Tweets", "Pending Tweets", "Unsafe Tweets", "Statistics", "User management"])

    with tab1:
        st.write("### All Tweets")
        with st.spinner("Loading tweets..."):
            all_tweets = fetch_all_tweets()  # Call your function to fetch tweets
        i = 0
        for tweet in all_tweets:
            # Display username in small text
            # Determine if the tweet should be blocked
            is_blocked = tweet.get('logreg_result', 0) == 1
                
            # Display username and tweet ID, add [BLOCKED] if necessary
            user_display = f"{tweet.get('user', 'Not available')} | tweet id: {tweet.get('tweet_id', '')}"
            if is_blocked:
                user_display += " <span style='color: #FF6347;'> [BLOCKED]<span>"
            st.markdown(f"<small>{user_display}</small>", unsafe_allow_html=True)

            # Display tweet content
            st.write(tweet.get('tweet', 'Not available'))

            # Display likes, retweets, and admin result in small text
            st.markdown(
                f"<small>Likes: {tweet.get('likes', 'Not available')} | Retweets: {tweet.get('retweets', 'Not available')} | Admin Result: {tweet.get('admin_result', 'Not available')}</small>",
                unsafe_allow_html=True
            )

            # Display the CNN result and probability
            cnn_prob = tweet.get('cnn_prob', 0) * 100  # Convert to percentage
            cnn_result_text = "Hatespeech" if tweet.get('cnn_result', 0) == 1 else "Not Hatespeech"
            st.markdown(
                f"<small>Model's decision: <span style='color: #FF6347;'>{cnn_result_text}</span> with probability {cnn_prob:.2f}%</small>",
                unsafe_allow_html=True
            )
            if not is_blocked and not tweet.get('cnn_result', 0) == 1:
                col1, col2 = st.columns([1,1])
                with col1:
                    if st.button('Mark as Safe', key=f"all_safe_{tweet['tweet_id'] + str(i)}"):
                        response = update_safety_status(tweet['tweet_id'], 0, 'admin')
                        st.write(response.get("message", "No message found"))
                    
                with col2:
                    if st.button('Mark as Unsafe', key=f"all_unsafe_{tweet['tweet_id'] + str(i)}"):
                        response = update_safety_status(tweet['tweet_id'], 1, 'admin')
                        st.write(response.get("message", "No message found"))

            i+=1
            st.write("---")

    with tab2:
        st.write("### Pending Tweets")
        pending_tabs = st.tabs(["User Reports", "Risky Tweets"])
        with pending_tabs[0]:
            st.write("Here are tweets reported by users and awaiting admin result.")
            with st.spinner("Loading tweets..."):
                reported_tweets = fetch_reported_tweets()
                for report in reported_tweets:
                    tweet = fetch_tweet_by_id(report['tweet_id'])
                    if tweet:
                        # Display tweet details
                        is_blocked = tweet.get('logreg_result', 0) == 1
                
                        # Display username and tweet ID, add [BLOCKED] if necessary
                        user_display = f"{tweet.get('user', 'Not available')} | tweet id: {tweet.get('tweet_id', '')}"
                        if is_blocked:
                            user_display += " <span style='color: #FF6347;'> [BLOCKED]<span>"
                        st.markdown(f"<small>{user_display}</small>", unsafe_allow_html=True)

                        # st.markdown(f"<small>{tweet.get('user_id', 'Not available')} \t\t |  tweet id: {report.get('tweet_id', '')}</small>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: #FF6347;'>{tweet.get('tweet', 'Not available')}</p>", unsafe_allow_html=True)
                        st.markdown(
                            f"<small>Likes: {tweet.get('likes', 'Not available')} \t\t| Retweets: {tweet.get('retweets', 'Not available')} \t\t| Admin Result: {tweet.get('admin_result', 'Not available')}</small>",
                            unsafe_allow_html=True
                        )
                        
                        # Display the CNN result and probability
                        cnn_prob = tweet.get('cnn_prob', 0) * 100  # Convert to percentage
                        cnn_result_text = "Hatespeech" if tweet.get('cnn_result', 0) == 1 else "Not Hatespeech"
                        st.markdown(
                            f"<small>Model's decision: <span style='color: #FF6347;'>{cnn_result_text}</span> with probability {cnn_prob:.2f}%</small>",
                            unsafe_allow_html=True
                        )

                        if not is_blocked and not tweet.get('cnn_result', 0) == 1:

                            col1, col2 = st.columns([1,1])
                            with col1:
                                if st.button('Mark as Safe', key=f"user_safe_{tweet['tweet_id'] + str(i)}"):
                                    response = update_safety_status(tweet['tweet_id'], 0, 'admin')
                                    st.write(response.get("message", "No message found"))
                                
                            with col2:
                                if st.button('Mark as Unsafe', key=f"user_unsafe_{tweet['tweet_id'] + str(i)}"):
                                    response = update_safety_status(tweet['tweet_id'], 1, 'admin')
                                    st.write(response.get("message", "No message found"))

                        st.write(f"Reported By: {report.get('user_id', 'Not available')}")
                        st.write("---")
                    i+=1

        with pending_tabs[1]:
            st.write("Here are tweets that had high probabilities (higher than 30%) with the cnn model but were not reported hate speech.")
            with st.spinner("Loading tweets..."):
                risky_tweets = fetch_risky_tweets()
                if risky_tweets:
                    i = 0
                    for tweet in risky_tweets:
                        st.markdown(f"<small>{tweet.get('user', 'Not available')} | tweet id: {tweet.get('tweet_id', '')}</small>", unsafe_allow_html=True)
                        st.write(f"<span style='color: #FF6347;'>{tweet.get('tweet', 'Not available')}</span>", unsafe_allow_html=True)
                        st.markdown(f"<small>Likes: {tweet.get('likes', 'Not available')} | Retweets: {tweet.get('retweets', 'Not available')} | Admin Result: {tweet.get('admin_result', 'Not available')}</small>", unsafe_allow_html=True)
                        
                        cnn_prob = tweet.get('cnn_prob', 0) * 100  # Convert to percentage
                        cnn_result_text = "Hatespeech" if tweet.get('cnn_result', 0) == 1 else "Not Hatespeech"
                        st.markdown(
                            f"<small>Model's decision: <span style='color: #FF6347;'>{cnn_result_text}</span> with probability {cnn_prob:.2f}%</small>",
                            unsafe_allow_html=True
                        )
                        if not is_blocked and not tweet.get('cnn_result', 0) == 1:

                            col1, col2 = st.columns([1,1])
                            with col1:
                                if st.button('Mark as Safe', key=f"risky_safe_{tweet['tweet_id'] + str(i)}"):
                                    response = update_safety_status(tweet['tweet_id'], 0, 'admin')
                                    st.write(response.get("message", "No message found"))
                                
                            with col2:
                                if st.button('Mark as Unsafe', key=f"risky_unsafe_{tweet['tweet_id'] + str(i)}"):
                                    response = update_safety_status(tweet['tweet_id'], 1, 'admin')
                                    st.write(response.get("message", "No message found"))
                        # st.markdown(f"<small>Logreg Prob: {tweet.get('logreg_prob', 'Not available')} | Logreg Result: {tweet.get('logreg_result', 'Not available')} | CNN Prob: {tweet.get('cnn_prob', 'Not available')} | CNN Result: {tweet.get('cnn_result', 'Not available')}</small>", unsafe_allow_html=True)
                        st.write("---")
                        i+=1
                else:
                    st.write("No risky tweets found.")

    with tab3:
        st.write("### Unsafe Tweets")
        st.write("Unsafe tweets will be displayed here.")
        unsafe_tabs = st.tabs(["Tweets marked by the model", "Tweets marked by admin"])
        with unsafe_tabs[0]:
            st.write("### Tweets marked by the model")
            cnn_unsafe_tweets = fetch_cnn_unsafe_tweets()
            if cnn_unsafe_tweets:
                for tweet in cnn_unsafe_tweets:
                    st.markdown(f"<small>{tweet.get('user', 'Not available')} | tweet id: {tweet.get('tweet_id', '')}</small>", unsafe_allow_html=True)
                    st.write(f"<span style='color:#FF6347;'>{tweet.get('tweet', 'Not available')}</span>", unsafe_allow_html=True)
                    st.markdown(f"<small>Likes: {tweet.get('likes', 'Not available')} | Retweets: {tweet.get('retweets', 'Not available')} | Admin Result: {tweet.get('admin_result', 'Not available')}</small>", unsafe_allow_html=True)
                    cnn_prob = tweet.get('cnn_prob', 0) * 100  # Convert to percentage
                    cnn_result_text = "Hatespeech" if tweet.get('cnn_result', 0) == 1 else "Not Hatespeech"
                    st.markdown(
                        f"<small>Model's decision: <span style='color: #FF6347;'>{cnn_result_text}</span> with probability {cnn_prob:.2f}%</small>",
                        unsafe_allow_html=True
                    )
                    st.write("---")
            else:
                st.write("No unsafe tweets marked by the model found.")

        with unsafe_tabs[1]:
            st.write("### Tweets marked by admin")
            admin_unsafe_tweets = fetch_admin_unsafe_tweets()
            if admin_unsafe_tweets:
                for tweet in admin_unsafe_tweets:
                    st.markdown(f"<small>{tweet.get('user', 'Not available')} | tweet id: {tweet.get('tweet_id', '')}</small>", unsafe_allow_html=True)
                    st.write(f"<span style='color:#FF6347;'>{tweet.get('tweet', 'Not available')}</span>", unsafe_allow_html=True)
                    st.markdown(f"<small>Likes: {tweet.get('likes', 'Not available')} | Retweets: {tweet.get('retweets', 'Not available')} | Admin Result: {tweet.get('admin_result', 'Not available')}</small>", unsafe_allow_html=True)
                    cnn_prob = tweet.get('cnn_prob', 0) * 100  # Convert to percentage
                    cnn_result_text = "Hatespeech" if tweet.get('cnn_result', 0) == 1 else "Not Hatespeech"
                    st.markdown(
                        f"<small>Model's decision: <span style='color: #FF6347;'>{cnn_result_text}</span> with probability {cnn_prob:.2f}%</small>",
                        unsafe_allow_html=True
                    )
                    st.write("---")
            else:
                st.write("No unsafe tweets marked by the admin found.")
    with tab4:
        st.write("### Statistics Tweets")
        st.write("Statistics will be displayed here.")
        with st.spinner("Loading data..."):
            # Fetch all tweets data
            tweets_data = fetch_all_tweets()
            if tweets_data:
                # Convert to DataFrame
                # Graph: Number of Tweets Over Time
                df = pd.DataFrame(tweets_data)

                # Convert 'created_at' to datetime
                df['created_at'] = pd.to_datetime(df['created_at'])

                # Filter unsafe tweets (those flagged by CNN or admin)
                unsafe_tweets = df[(df['cnn_result'] == 1) | (df['admin_result'] == 1)]

                # Set 'created_at' as index for resampling
                df_with_time = df.set_index('created_at')
                unsafe_tweets.set_index('created_at', inplace=True)

                # Determine the time span of the data
                time_span = df_with_time.index.max() - df_with_time.index.min()
                print("Time span: ", time_span)
                
                # Set dynamic resampling frequency
                if time_span <= pd.Timedelta(hours=1):
                    resample_freq = '3min'
                elif time_span <= pd.Timedelta(hours=3):
                    resample_freq = '30min'
                else:
                    resample_freq = '1h'

                # Resample data
                total_tweets_over_time = df_with_time.resample(resample_freq).size()
                unsafe_tweets_over_time = unsafe_tweets.resample(resample_freq).size()

                # Plot the number of total and unsafe tweets over time
                fig, ax = plt.subplots(figsize=(12, 6))  # Specify figure size
                total_tweets_over_time.plot(ax=ax, label='Total Tweets', linestyle='--')
                unsafe_tweets_over_time.plot(ax=ax, label='Unsafe Tweets', marker='o', linestyle='-')

                ax.set_title('Number of Tweets Over Time')
                ax.set_xlabel('Time')
                ax.set_ylabel('Number of Tweets')
                ax.legend()
                ax.grid(True)

                # Rotate x-axis labels for better readability
                plt.xticks(rotation=45)

                # Display plot in Streamlit
                st.pyplot(fig)

                # Graph 2: Comparison of Unsafe Tweets Identified by CNN vs Admin Over Time
                st.write("#### Comparison of Unsafe Tweets Identified by CNN vs Admin Over Time")
 
                all_changes = fetch_safety_status_changes()
                changes_df = pd.DataFrame(all_changes)
                changes_df['changed_at'] = pd.to_datetime(changes_df['changed_at'])

                # Filter changes by source
                cnn_changes = changes_df[changes_df['change_source'] == 'cnn']
                admin_changes = changes_df[changes_df['change_source'] == 'admin']
                # Resample and plot
                cnn_unsafe_changes = cnn_changes.resample('2min', on='changed_at').size()
                admin_unsafe_changes = admin_changes.resample('2min', on='changed_at').size()

                fig, ax = plt.subplots()
                cnn_unsafe_changes.plot(ax=ax, label='CNN Unsafe Tweets')
                admin_unsafe_changes.plot(ax=ax, label='Admin Unsafe Tweets')

                ax.set_xlabel('Date')
                ax.set_ylabel('Number of Unsafe Tweets')
                ax.legend()
                st.pyplot(fig)

                # Graph 3: Distribution of CNN Probability Scores for Unsafe Tweets
                st.write("#### Distribution of Model's Probability Scores for Unsafe Tweets")
                cnn_prob_scores = df[df['cnn_result'] == 1]['cnn_prob']
                fig, ax = plt.subplots()
                sns.histplot(cnn_prob_scores, bins=20, kde=True, ax=ax)
                ax.set_xlabel('Model Probability Score')
                ax.set_ylabel('Frequency')
                st.pyplot(fig)


                # Graph 4: User behavior

                # Convert to DataFrame
                df = pd.DataFrame(tweets_data)
                # Convert 'created_at' to datetime
                df['created_at'] = pd.to_datetime(df['created_at'])

                # Filter hate speech tweets
                blocked_realtime = df[df['logreg_result'] == 1]
                blocked_by_model = df[df['cnn_result'] == 1]
                blocked_by_admin = df[df['admin_result'] == 1]

                # Group by user and count tweets
                blocked_realtime_counts = blocked_realtime.groupby('user').size().sort_values(ascending=False)
                blocked_by_model_counts = blocked_by_model.groupby('user').size().sort_values(ascending=False)
                blocked_by_admin_counts = blocked_by_admin.groupby('user').size().sort_values(ascending=False)
                
                # Get top users
                top_users = list(set(blocked_realtime_counts.index) |
                                set(blocked_by_model_counts.index) |
                                set(blocked_by_admin_counts.index))

                # Create a DataFrame for the top users
                top_users_df = pd.DataFrame({
                    'user': top_users
                }).set_index('user')

                # Add counts to the DataFrame
                top_users_df['Blocked in Real-time'] = top_users_df.index.map(blocked_realtime_counts).fillna(0)
                top_users_df['Blocked by Model'] = top_users_df.index.map(blocked_by_model_counts).fillna(0)
                top_users_df['Blocked by Admin'] = top_users_df.index.map(blocked_by_admin_counts).fillna(0)

                # Calculate total counts
                top_users_df['Total'] = top_users_df.sum(axis=1)
                
                # Sort by total counts
                top_users_df = top_users_df.sort_values(by='Total', ascending=False)
                
                # Drop the 'Total' column as we don't need it in the graph
                top_users_df.drop(columns=['Total'], inplace=True)

                st.write("#### Users with unsafe behavior")

                # Create tabs in Streamlit
                tab1, tab2, tab3 = st.tabs(["Blocked in Real-time", "Marked by Model", "Marked by Admin"])

                # Tab 1: Blocked in Real-time
                with tab1:
                    st.write('##### Blocked in Real-time')
                    buf = plot_grouped_bar_chart(top_users_df[['Blocked in Real-time']], 'Blocked in Real-time')
                    st.image(buf)

                # Tab 2: Blocked by Model
                with tab2:
                    st.write('##### Marked by Model')
                    buf = plot_grouped_bar_chart(top_users_df[['Blocked by Model']], 'Marked by Model')
                    st.image(buf)

                # Tab 3: Blocked by Admin
                with tab3:
                    st.header('Marked by Admin')
                    buf = plot_grouped_bar_chart(top_users_df[['Blocked by Admin']], 'Marked by Admin')
                    st.image(buf)
            else:
                st.write("No data available for generating statistics.")
                print("Found no data.")
                

    with tab5:
        # Admin functionalities section
        st.write("## Admin Functions")

        # Block User
        st.write("### Block User")
        block_user_id = st.text_input("User ID to block")
        if st.button("Block User"):
            if block_user_id:
                block_response = admin_manager.block_user(block_user_id)
                if block_response:
                    st.success(f"User {block_user_id} blocked successfully.")
                else:
                    st.error(f"Failed to block user {block_user_id}.")
            else:
                st.error("Please provide a User ID to block.")

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

# Function to plot the grouped bar chart
def plot_grouped_bar_chart(df, title):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot bars
    df.plot(kind='bar', ax=ax)
    
    # Set titles and labels
    ax.set_title(title)
    ax.set_xlabel('Users')
    ax.set_ylabel('Number of Hate Speech Tweets')
    ax.grid(True)
    plt.xticks(rotation=0)
    
    # Save plot to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    
    return buf
