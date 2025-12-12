import streamlit as st
import os
from classes import UserServices
from data_access import _get_conn
from functions import generate_recommendations

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


st.sidebar.title("Menu")
page = st.sidebar.radio(
    "Navigate",
    ["Home", "Attractions", "Recommendations"]
)

if page == "Home":
    st.header("Welcome")
    st.write("Logged in as:", st.session_state.get("user"))

elif page == "Attractions":
    st.header("Browse Attractions")
    # list_attractions UI here

elif page == "Recommendations":
    st.header("Your Recommendations")

    username = st.session_state.get("user")
    if not username:
        st.error("Please log in first.")
        st.stop()

    city = st.text_input("Filter by city (optional)")
    top_k = st.slider("Number of recommendations", 1, 20, 10)

    if st.button("Generate Recommendations"):
        result = generate_recommendations({
            "username": username,
            "city": city or None,
            "top_k": top_k
        })

        if result["success"]:
            if result["recommendations"]:
                st.dataframe(result["recommendations"])
            else:
                st.info("No recommendations found.")
        else:
            st.error(result["error"])
