import streamlit as st
from datetime import date
import json
import re
from difflib import get_close_matches
import pandas as pd
from openai import OpenAI
import os

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Health Coach", layout="centered")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DATA_FILE = "health_data.json"

# ---------------- LOAD/SAVE ----------------
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            for k, v in data.items():
                st.session_state[k] = v
    except:
        pass

def save_data():
    data = {
        "daily_cal": st.session_state.daily_cal,
        "daily_pro": st.session_state.daily_pro,
        "history": st.session_state.history,
        "custom_foods": st.session_state.custom_foods,
        "chat_history": st.session_state.chat_history
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# ---------------- INIT ----------------
if 'loaded' not in st.session_state:
    load_data()
    st.session_state.loaded = True

if 'daily_cal' not in st.session_state: st.session_state.daily_cal = 0
if 'daily_pro' not in st.session_state: st.session_state.daily_pro = 0
if 'custom_foods' not in st.session_state: st.session_state.custom_foods = {}
if 'history' not in st.session_state: st.session_state.history = {}
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("Settings")

    weight = st.number_input("Weight (kg)", 40, 150, 70)
    goal = st.selectbox("Goal", ["Weight Loss", "Weight Gain", "Muscle Building"])

    if goal == "Weight Loss":
        limit = weight * 20
    elif goal == "Weight Gain":
        limit = weight * 35
    else:
        limit = weight * 30

    st.metric("Calories", f"{st.session_state.daily_cal}/{int(limit)}")
    st.metric("Protein", f"{st.session_state.daily_pro} g")

# ---------------- FOOD DATABASE ----------------
food_db = {
    "chai": {"tags": ["chai", "tea"], "cal": 90, "pro": 2},
    "paratha": {"tags": ["paratha", "pratha"], "cal": 290, "pro": 6},
    "egg": {"tags": ["egg", "anda"], "cal": 78, "pro": 7},
    "biryani": {"tags": ["biryani", "rice"], "cal": 480, "pro": 18},
}

food_db.update(st.session_state.custom_foods)

# ---------------- MAIN ----------------
st.title("AI Health Coach")

query = st.text_input("What did you eat today?").lower()

def extract_qty(food, text):
    match = re.search(r'(\d+)\s*' + food, text)
    return int(match.group(1)) if match else 1

if query:
    total_cal, total_pro = 0, 0

    for word in query.split():
        match = get_close_matches(word, food_db.keys(), n=1, cutoff=0.7)
        if match:
            food = match[0]
            data = food_db[food]
            qty = extract_qty(food, query)

            total_cal += data['cal'] * qty
            total_pro += data['pro'] * qty

    if total_cal > 0:
        st.success(f"Total: {total_cal} kcal | {total_pro} g protein")

        # AI AUTO FEEDBACK
        try:
            prompt = f"User ate {query}. Calories {total_cal}, Protein {total_pro}. Goal is {goal}. Give short advice."

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            st.info("AI Suggestion: " + response.choices[0].message.content)

        except:
            st.warning("AI not connected")

        if st.button("Add to Progress"):
            st.session_state.daily_cal += total_cal
            st.session_state.daily_pro += total_pro

            today = str(date.today())
            if today not in st.session_state.history:
                st.session_state.history[today] = {"cal": 0, "pro": 0}

            st.session_state.history[today]["cal"] += total_cal
            st.session_state.history[today]["pro"] += total_pro

            save_data()
            st.rerun()

# ---------------- CHAT ----------------
st.divider()
st.subheader("AI Coach Chat")

for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

user_input = st.chat_input("Ask your coach")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.chat_history
        )

        reply = response.choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

        with st.chat_message("assistant"):
            st.write(reply)

    except:
        st.error("AI error")

    save_data()

# ---------------- ANALYTICS ----------------
st.divider()
st.subheader("Progress")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history).T
    st.line_chart(df)

# ---------------- CREDIT ----------------
st.markdown("---")
st.markdown("Developed by Abbas Ali")