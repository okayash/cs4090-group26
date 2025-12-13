import streamlit as st
from data_access import validate_user_credentials
from functions import generate_recommendations

st.title("CLIO Login")

username = st.text_input("Username: ")
password = st.text_input("Password: ", type="password")

if st.button("Login"):
    if validate_user_credentials(username, password):
        st.success("Login successful!")
        st.session_state["user"] = username
    else:
        st.error("User not found. Please check username or create a new account.")

st.sidebar.title("Menu")
page = st.sidebar.radio("Navigate", ["Home", "Attractions", "Recommendations"])

if page == "Home":
    st.header("Welcome")
    st.write("Logged in as:", st.session_state.get("user"))

elif page == "Attractions":
    st.header("Browse Attractions")
    # later: call functions.list_attractions(...) and show results

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
