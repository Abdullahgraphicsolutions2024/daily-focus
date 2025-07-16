
import streamlit as st
import json, os
from datetime import date, datetime, timedelta
import time

st.set_page_config(page_title="Daily Focus Pro", layout="centered")

st.markdown("""
<style>
body { background-color: #0d1b2a; color: #ffffff; font-family: "Alberta", sans-serif; font-size:16px; }
h1, h2, h3 {
    color: #00d4ff;
    font-family: "Alberta", sans-serif;
}
input, select, .stTextInput > div > div > input {
    background-color: #1b263b !important;
    color: white !important;
    border-radius: 8px !important;
}
.stButton>button {
    background-color: #00d4ff;
    color: black;
    border-radius: 8px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("Daily Focus Pro")
username = st.text_input("Username")
password = st.text_input("Password", type="password")
auth_file = f"{username}_tasks.json"

if username and password == "1234":
    def load_tasks():
        if os.path.exists(auth_file):
            with open(auth_file, "r") as f:
                return json.load(f)
        return []

    def save_tasks(tasks):
        with open(auth_file, "w") as f:
            json.dump(tasks, f)

    if "tasks" not in st.session_state:
        st.session_state.tasks = load_tasks()

    st.subheader("Filter Tasks by Category")
    filter_cat = st.selectbox("Choose category", ["All", "Work", "Study", "Personal"])

    st.markdown("### Task List")
    filtered = [t for t in st.session_state.tasks if filter_cat == "All" or t["category"] == filter_cat]
    for i, task in enumerate(filtered):
        col1, col2, col3 = st.columns([0.05, 0.7, 0.25])
        with col1:
            task["done"] = st.checkbox("", value=task["done"], key=f"check_{i}")
        with col2:
            st.text_input("", value=f"{task['category']} - {task['text']}", disabled=True, key=f"label_{i}")
        with col3:
            st.date_input("", value=date.fromisoformat(task["deadline"]), disabled=True, key=f"date_{i}")

    st.markdown("### Add New Task")
    new_task = st.text_input("Task")
    new_cat = st.selectbox("Category", ["Work", "Study", "Personal"])
    new_deadline = st.date_input("Deadline", value=date.today())

    if st.button("Add Task"):
        if new_task.strip():
            st.session_state.tasks.append({
                "text": new_task.strip(),
                "done": False,
                "category": new_cat,
                "deadline": str(new_deadline)
            })
            save_tasks(st.session_state.tasks)
            st.experimental_rerun()
        else:
            st.warning("Please enter a valid task.")

    if len(st.session_state.tasks) > 0:
        st.markdown("### Remove Task by Number")
        remove_index = st.number_input("Enter task number (1-based)", min_value=1, max_value=len(st.session_state.tasks))
        if st.button("Remove Task"):
            removed = st.session_state.tasks.pop(remove_index - 1)
            save_tasks(st.session_state.tasks)
            st.success(f"Removed: {removed['text']}")
            st.experimental_rerun()

    st.markdown("### Reminder Notifications")
    today = date.today()
    for task in st.session_state.tasks:
        deadline = date.fromisoformat(task["deadline"])
        if not task["done"] and (deadline - today).days == 1:
            st.info(f"Reminder: Task '{task['text']}' is due tomorrow!")
        elif not task["done"] and deadline <= today:
            st.error(f"Alert: Task '{task['text']}' is due or overdue!")

    st.markdown("### Focus Timer (Minutes)")
    timer_min = st.slider("Select Minutes", 1, 60, 25)
    if st.button("Start Timer"):
        st.info(f"Timer started for {timer_min} minutes.")
        with st.empty():
            for i in range(timer_min * 60, 0, -1):
                mins, secs = divmod(i, 60)
                st.markdown(f"## {mins:02d}:{secs:02d}")
                time.sleep(1)
            st.success("Time's up!")

    save_tasks(st.session_state.tasks)
    st.markdown("---")
    st.caption("© 2025 Daily Focus Pro")
else:
    if username and password:
        st.error("Incorrect password. Hint: 1234")
    st.warning("Enter login credentials to continue.")
