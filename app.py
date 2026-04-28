import streamlit as st
from datetime import date
import pandas as pd
import re
import json
import os

# --- 1. CONFIG ---
st.set_page_config(page_title="Gemini Health Ultra", page_icon="🥗", layout="centered")

DATA_FILE = "health_master_data.json"

# --- 2. STORAGE LOGIC ---
def load_all_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f: return json.load(f)
        except: return {"profile": {}, "days_log": {}, "current_day": 1}
    return {"profile": {}, "days_log": {}, "current_day": 1}

def save_all_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

if 'app_data' not in st.session_state:
    st.session_state.app_data = load_all_data()

db = st.session_state.app_data

# --- 3. FOOD DATABASE ---
food_db = {
    "paratha": {"cal": 290, "tags": ["paratha", "pratha"]},
    "anda": {"cal": 78, "tags": ["egg", "anda", "eggs"]},
    "biryani": {"cal": 450, "tags": ["biryani", "pulao", "rice"]},
    "roti": {"cal": 110, "tags": ["roti", "chapati", "phulka"]},
    "daal": {"cal": 180, "tags": ["daal", "dal"]},
    "chicken": {"cal": 300, "tags": ["chicken", "murghi", "tikka"]},
    "chai": {"cal": 90, "tags": ["chai", "tea"]},
    "fruit": {"cal": 80, "tags": ["fruit", "apple", "banana"]}
}

# --- 4. MAIN INTERFACE ---
st.title("👨‍⚕️ Gemini Health Engine")

# STEP 1: Agar Profile nahi bani to seedha saamne form dikhao
if not db.get("profile"):
    st.subheader("👋 Welcome! Pehle apni details enter karein")
    with st.container():
        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            u_weight = st.number_input("Weight (kg)", 40, 150, 70)
            u_height = st.number_input("Height (cm)", 120, 220, 170)
        with c2:
            u_age = st.number_input("Age", 15, 80, 25)
            u_goal = st.selectbox("Goal", ["Weight Loss", "Muscle Gain"])
        
        if st.button("🚀 Start My 28-Day Challenge", use_container_width=True):
            # Mifflin-St Jeor Formula
            target = (10*u_weight + 6.25*u_height - 5*u_age + 5) * 1.2
            db["profile"] = {
                "target": int(target - 500 if u_goal == "Weight Loss" else target + 500),
                "goal": u_goal
            }
            save_all_data(db)
            st.rerun()

# STEP 2: Agar Profile bani hui hai to Dashboard dikhao
else:
    day = db["current_day"]
    day_key = f"day_{day}"
    
    if day_key not in db["days_log"]:
        db["days_log"][day_key] = {"cal": 0, "water": 0, "meals": []}

    # Header Card
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e2130 0%, #2b2f48 100%); padding: 25px; border-radius: 15px; border: 1px solid #4CAF50; color: white; text-align: center;">
            <h1 style="margin:0;">🏆 Challenge Day {day} of 28</h1>
            <p style="margin:5px;">Goal: {db['profile']['goal']} | Target: {db['profile']['target']} kcal</p>
        </div>
    """, unsafe_allow_html=True)

    st.write("") # Spacer

    # Action Area
    col_meal, col_water = st.columns(2)
    
    with col_meal:
        st.subheader("🍽️ Meal Tracker")
        query = st.text_input("Aap ne kya khaya?", placeholder="e.g. 2 anda aur 1 roti", key="food_q").lower()
        if query:
            for item, info in food_db.items():
                for tag in info["tags"]:
                    if tag in query:
                        num = re.search(r'(\d+)', query)
                        qty = int(num.group(1)) if num else 1
                        total_cal = info['cal'] * qty
                        if st.button(f"Add {qty} {item.capitalize()} ({total_cal} kcal)", use_container_width=True):
                            db["days_log"][day_key]["cal"] += total_cal
                            save_all_data(db)
                            st.success("Added!")
                            st.rerun()

    with col_water:
        st.subheader("💧 Hydration")
        glasses = db["days_log"][day_key]["water"]
        st.markdown(f"**{glasses} / 12** Glasses")
        if st.button("➕ Drink 1 Glass Water", use_container_width=True):
            db["days_log"][day_key]["water"] += 1
            save_all_data(db)
            st.rerun()

    st.divider()

    # Progress Summary
    st.subheader("📊 Today's Progress")
    curr_cal = db["days_log"][day_key]["cal"]
    t_cal = db["profile"]["target"]
    
    c1, c2 = st.columns(2)
    c1.metric("Calories Consumed", f"{curr_cal} / {t_cal} kcal")
    c1.progress(min(curr_cal / t_cal, 1.0))
    
    c2.metric("Water Intake", f"{glasses} / 12 Glasses")
    c2.progress(min(glasses / 12, 1.0))

    st.write("")
    if st.button("🏁 FINISH DAY & SAVE PROGRESS", use_container_width=True):
        if day < 28:
            db["current_day"] += 1
            save_all_data(db)
            st.balloons()
            st.rerun()
        else:
            st.success("🎉 28-DAY CHALLENGE COMPLETED!")

    # Reset Option (Main Page ke niche)
    with st.expander("⚙️ Settings (Reset Data)"):
        if st.button("Delete Everything & Restart"):
            db = {"profile": {}, "days_log": {}, "current_day": 1}
            save_all_data(db)
            st.rerun()

st.caption("Integrated Health Engine V30.0 | No Sidebar Required")
