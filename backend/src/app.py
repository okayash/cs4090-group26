import streamlit as st
import os
from classes import UserServices
from data_access import _get_conn

def validate_user(username, password) -> bool:
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT username FROM User WHERE username = %s AND password = %s", (username, password))
        result = cur.fetchone()
        return result is not None
    finally:
        cur.close()
        conn.close()

st.title("ClIO Login")

username = st.text_input("Username: ")
password = st.text_input("Password: ", type="password")

if st.button("Login"):
    if validate_user(username, password):
        st.success("Login successful!")
        st.session_state["user"] = username
    else:
        st.error("User not found. Please check username or create a new account.")
