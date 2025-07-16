
import streamlit as st

st.set_page_config(page_title="Daily Focus LMS", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    with st.form("Login"):
        st.subheader("Login to Daily Focus LMS")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        if submit:
            if username == "admin" and password == "1234":
                st.session_state.logged_in = True
                st.success("Login successful")
                st.experimental_rerun()
            else:
                st.error("Invalid credentials")

if not st.session_state.logged_in:
    login()
else:
    st.title("Welcome to Daily Focus LMS")
    st.markdown("Use the left sidebar to navigate between **Tasks**, **Analytics**, and **Settings**.")
