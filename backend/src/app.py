import streamlit as st
import os
from classes import UserServices
from data_access import _get_conn

def validate_user(username):
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT username FROM User WHERE username = %s", (username,))
        result = cur.fetchone()
        return result is not None
    finally:
        cur.close()
        conn.close()

st.title("ClIO Login")

username = st.text_input("Username: ")

if st.button("Login"):
    if validate_user(username):
        st.success("Login successful!")
        st.session_state["user"] = username
    else:
        st.error("User not found. Please check username or create a new account.")
