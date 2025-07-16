
import streamlit as st
import json
import os
from datetime import date

TASK_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f)

if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

st.title(" Task Manager")

st.subheader("Filter by Category")
filter_cat = st.selectbox("Category", ["All", "Work", "Study", "Personal"])
filtered = [t for t in st.session_state.tasks if filter_cat == "All" or t["category"] == filter_cat]

for i, task in enumerate(filtered):
    col1, col2, col3 = st.columns([0.1, 0.6, 0.3])
    with col1:
        task["done"] = st.checkbox("", value=task["done"], key=f"done_{i}")
    with col2:
        st.text_input("", value=f"{task['category']} - {task['text']}", disabled=True, key=f"txt_{i}")
    with col3:
        st.date_input("", value=date.fromisoformat(task["deadline"]), disabled=True, key=f"date_{i}")

st.divider()
st.subheader("Add New Task")
text = st.text_input("Task")
cat = st.selectbox("Category", ["Work", "Study", "Personal"])
deadline = st.date_input("Deadline", value=date.today())

if st.button("Add Task"):
    if text.strip():
        st.session_state.tasks.append({
            "text": text.strip(),
            "done": False,
            "category": cat,
            "deadline": str(deadline)
        })
        save_tasks(st.session_state.tasks)
        st.success("Task Added!")
        st.experimental_rerun()

if len(st.session_state.tasks) > 0:
    st.subheader("Remove Task by Number")
    idx = st.number_input("Task number", 1, len(st.session_state.tasks))
    if st.button("Remove Task"):
        removed = st.session_state.tasks.pop(idx - 1)
        save_tasks(st.session_state.tasks)
        st.success(f"Removed: {removed['text']}")
        st.experimental_rerun()

save_tasks(st.session_state.tasks)
