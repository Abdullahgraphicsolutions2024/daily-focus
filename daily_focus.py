
import streamlit as st
from datetime import date
import json
import os

st.set_page_config(page_title="Daily Focus LMS", layout="centered")

# Session init
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "page" not in st.session_state:
    st.session_state.page = "Login"

# Dummy user
USER = "admin"
PASS = "1234"
DATA_FILE = "tasks.json"

# Load/Save
def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f)

# Sidebar navigation
def sidebar():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Tasks", "Analytics", "Logout"])
    st.session_state.page = page

# Login Page
def login():
    st.title("Welcome to Daily Focus LMS")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == USER and password == PASS:
            st.session_state.authenticated = True
            st.session_state.page = "Dashboard"
            st.success("Logged in successfully.")
        else:
            st.error("Invalid credentials")

# Dashboard Page
def dashboard():
    st.title("📋 Dashboard")
    st.info("Welcome to your productivity dashboard.")
    st.metric("Tasks Today", len([t for t in load_tasks() if t["date"] == str(date.today())]))
    st.metric("Total Tasks", len(load_tasks()))

# Tasks Page
def tasks_page():
    st.title("🗂️ Tasks")
    tasks = load_tasks()

    st.subheader("Your Tasks")
    for i, t in enumerate(tasks):
        st.checkbox(f"{t['title']} - Due: {t['date']}", key=i)

    st.subheader("Add New Task")
    title = st.text_input("Task Title")
    deadline = st.date_input("Deadline", value=date.today())
    if st.button("Add Task"):
        tasks.append({"title": title, "date": str(deadline)})
        save_tasks(tasks)
        st.success("Task added.")
        st.experimental_rerun()

# Analytics Page
def analytics():
    st.title("📈 Analytics")
    tasks = load_tasks()
    dates = {}
    for t in tasks:
        dates[t["date"]] = dates.get(t["date"], 0) + 1
    st.bar_chart(dates)

# Logout Page
def logout():
    st.session_state.authenticated = False
    st.session_state.page = "Login"
    st.success("Logged out successfully.")

# Theme Styling
st.markdown("""
<style>
body {
    background-color: #0c1a24;
    color: white;
    font-family: 'Alberto', sans-serif;
}
h1, h2, h3 {
    color: #ffffff;
}
</style>
"", unsafe_allow_html=True)

# Routing
if not st.session_state.authenticated:
    login()
else:
    sidebar()
    if st.session_state.page == "Dashboard":
        dashboard()
    elif st.session_state.page == "Tasks":
        tasks_page()
    elif st.session_state.page == "Analytics":
        analytics()
    elif st.session_state.page == "Logout":
        logout()
