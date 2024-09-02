import streamlit as st
import mysql.connector
import pandas as pd

# Function to connect to the database
def connect_to_db():
    return mysql.connector.connect(
        host="my.cht77.com",
        port=13306,
        user="ashad",
        password="password",
        database="advisor_LLM_chat"
    )



# Function to load data from the database
def load_data(query):
    conn = connect_to_db()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Load data from each table
def load_chat_messages():
    query = "SELECT * FROM chat_messages ORDER BY timestamp"
    return load_data(query)

def load_quiz_attempts():
    query = "SELECT * FROM QuizAttempts"
    return load_data(query)

def load_attempt_details():
    query = "SELECT * FROM AttemptDetails"
    return load_data(query)

# Streamlit app
st.title("Database Viewer")

# Display data from chat_messages table, ordered by timestamp
st.header("Chat Messages")
chat_messages_df = load_chat_messages()
st.dataframe(chat_messages_df)

# Display data from QuizAttempts table
st.header("Quiz Attempts")
quiz_attempts_df = load_quiz_attempts()
st.dataframe(quiz_attempts_df)

# Display data from AttemptDetails table
st.header("Attempt Details")
attempt_details_df = load_attempt_details()
st.dataframe(attempt_details_df)




# Load unique user_id from AttemptDetails via QuizAttempts
def load_unique_user_ids():
    query = """
    SELECT DISTINCT qa.user_id
    FROM QuizAttempts qa
    JOIN AttemptDetails ad ON qa.attempt_id = ad.attempt_id
    WHERE ad.is_correct = 0
    """
    return load_data(query)

# Custom view function to display filtered results
def load_custom_view(user_id):
    query = f"""
    SELECT 
        ad.question_number, 
        qa.attempt_number, 
        ad.chosen_option
    FROM 
        QuizAttempts qa
    JOIN 
        AttemptDetails ad ON qa.attempt_id = ad.attempt_id
    WHERE 
        qa.user_id = '{user_id}' AND 
        ad.is_correct = 0
    """
    return load_data(query)

# Streamlit app
st.title("Database Viewer")

# Custom view
st.header("Custom View: Incorrect Answers by User")
unique_user_ids = load_unique_user_ids()["user_id"].tolist()

selected_user_id = st.selectbox("Select User ID", unique_user_ids)

if st.button("Show Results"):
    custom_view_df = load_custom_view(selected_user_id)
    st.dataframe(custom_view_df)

# Add a refresh button to reload the data
if st.button("Refresh Data"):
    custom_view_df = load_custom_view(selected_user_id)
    st.dataframe(custom_view_df)
