
import streamlit as st
import json
import os
import matplotlib.pyplot as plt

TASK_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            return json.load(f)
    return []

tasks = load_tasks()

st.title(" Task Analytics")

if tasks:
    total = len(tasks)
    completed = sum(t["done"] for t in tasks)
    pending = total - completed

    st.metric("Total Tasks", total)
    st.metric("Completed", completed)
    st.metric("Pending", pending)

    fig, ax = plt.subplots()
    ax.pie([completed, pending], labels=["Completed", "Pending"], colors=["#00b894", "#d63031"], autopct="%1.1f%%")
    ax.set_title("Task Completion Ratio")
    st.pyplot(fig)
else:
    st.info("No tasks found.")
