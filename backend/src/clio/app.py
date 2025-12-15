
import streamlit as st

from clio.functions import (
    create_user,
    list_attractions,
    list_saved_recommendations,
    update_user_interests,
    generate_recommendations,
    validate_user_credentials,
    list_interests,
    get_user_interest_names,
    save_recommendations
)

def fee_label(v) -> str:
    try:
        return "Paid Experience" if float(v or 0) >= 1 else "Free Entry"
    except Exception:
        return "Unknown"

def main():
    st.set_page_config(page_title="CLIO", layout="wide")

    def require_login():
        if not st.session_state.get("username"):
            st.warning("Please log in first.")
            st.stop()

    def logout():
        st.session_state["username"] = None
        st.session_state["logged_in"] = False

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "username" not in st.session_state:
        st.session_state["username"] = None

    if "page" not in st.session_state:
        st.session_state["page"] = "Login"

    cols = st.columns(5)
    if cols[0].button("Login", key="login_nav_btn"): st.session_state["page"] = "Login"
    if cols[1].button("Create Account", key="create_nav_btn"): st.session_state["page"] = "Create Account"
    if cols[2].button("Profile and Interests", key="profile_nav_btn"): st.session_state["page"] = "Profile"
    if cols[3].button("Browse Attractions", key="browse_nav_btn"): st.session_state["page"] = "Browse Attractions"
    if cols[4].button("Recommendations", key="recs_nav_btn"): st.session_state["page"] = "Recommendations"

    page = st.session_state["page"]


    if st.session_state.get("logged_in"):
        st.sidebar.success(f"Logged in as {st.session_state['username']}")
        if st.sidebar.button("Logout"):
            logout()

    if page == "Login":
        st.header("Login")
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Login", key="login_btn"):
            ok = validate_user_credentials(u, p)
            if ok:
                st.session_state["logged_in"] = True
                st.session_state["username"] = u
                st.success("Logged in!")
            else:
                st.error("Invalid username/password.")


    elif page == "Create Account":
        st.header("Create Account")

        username = st.text_input("Username *")
        first = st.text_input("First name *")
        last = st.text_input("Last name *")
        email = st.text_input("Email")
        age = st.text_input("Age")
        home_city = st.text_input("Location (City)")
        password = st.text_input("Password", type="password") 

        if st.button("Create!", key="create_btn"):
            payload = {
                "username": username,
                "first_name": first,
                "last_name": last,
                "email": email or None,
                "age": age or None,
                "home_city": home_city or None,
                "password": password, 
            }

            res = create_user(payload)

            if res.get("success"):
                st.success("Account created! You may log in now.")
            else:
                st.error(res.get("error", "Account creation failed."))

    elif page == "Profile":
        st.header("Profile")
        require_login()
        username = st.session_state["username"]

        st.subheader("Your Interests")

        res = list_interests()
        if not res.get("success"):
            st.error(res.get("error", "Failed to load interests."))
        else:
            all_interests = res["interests"]  
            all_names = [x["name"] for x in all_interests]
            name_to_id = {x["name"]: x["interest_id"] for x in all_interests}

            cur_res = get_user_interest_names(username)
            current = cur_res["interest_names"] if cur_res.get("success") else []

            selected = st.multiselect("Pick interests", all_names, default=current)

            if st.button("Save Interests", key="save_interests_btn"):
                selected_ids = [name_to_id[n] for n in selected]
                save_res = update_user_interests({"username": username, "interests": selected_ids})

                if save_res.get("success"):
                    st.success("Interests saved!")
                else:
                    st.error(save_res.get("error", "Failed to save interests."))

    elif page == "Browse Attractions":
        st.header("Browse Attractions")

        city = st.text_input("City Filter (Optional)", key="browse_city")

        if st.button("Load Attractions", key="load_attractions_btn"):
            res = list_attractions({"city": city or None})

            if res.get("success"):
                data = res.get("attractions", [])

                if data:
                    for r in data:
                        r["fee"] = fee_label(r.get("price"))
                        r.pop("price", None)

                    st.dataframe(data, use_container_width=True)
                else:
                    st.info("No attractions found.")
            else:
                st.error(res.get("error", "Failed to load attractions."))


    elif page == "Recommendations":
        st.header("Your Recommendations")
        require_login()

        username = st.session_state["username"]
        city = st.text_input("City filter (optional)", key="recs_city")
        top_k = st.slider("How many recommendations?", 1, 20, 10, key="recs_topk")

        if "last_recs" not in st.session_state:
            st.session_state["last_recs"] = []
        if st.button("Generate", key="generate_recs_btn"):
            res = generate_recommendations({
                "username": username,
                "city": city or None,
                "top_k": top_k
            })

            if res.get("success"):
                st.session_state["last_recs"] = res.get("recommendations", [])
                if not st.session_state["last_recs"]:
                    st.info(res.get("message", "No matches found."))
            else:
                st.session_state["last_recs"] = []
                st.error(res.get("error", "Recommendation generation failed."))

        recs = st.session_state.get("last_recs", [])
        if recs:
            for r in recs:
                r["fee"] = fee_label(r.get("price"))
                r.pop("price", None)

            st.dataframe(recs, use_container_width=True)

            if st.button("Save these recommendations to my account", key="save_recs_btn"):
                save_res = save_recommendations({
                    "username": username,
                    "recommendations": recs
                })

                if save_res.get("success"):
                    st.success("Saved recommendations!")
                else:
                    st.error(save_res.get("error", "Failed to save recommendations."))
        if st.button("Load my saved recommendations", key="load_saved_recs_btn"):
            res_saved = list_saved_recommendations({"username": username})
            if res_saved.get("success"):
                saved = res_saved.get("recommendations", [])
                if saved:
                    st.dataframe(saved, use_container_width=True)
                else:
                    st.info("You don't have any recommendations. Please generate and save some first.")
            else:
                st.error(res_saved.get("error", "Failed to load saved recommendations."))

            # repeated save bug, need to fix tmwww ughughguhughug