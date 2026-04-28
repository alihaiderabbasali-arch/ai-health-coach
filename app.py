import streamlit as st
from datetime import date
import pandas as pd
import re
import json
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Sehat28 - Your Health Partner", page_icon="🥗", layout="centered")

# Data file (Isay kabhi mat badalna taake user ka data save rahe)
DATA_FILE = "sehat28_master_data.json"

# --- 2. STORAGE ENGINE ---
def load_all_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return {"profile": {}, "days_log": {}, "current_day": 1}
    return {"profile": {}, "days_log": {}, "current_day": 1}

def save_all_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

if 'app_data' not in st.session_state:
    st.session_state.app_data = load_all_data()

db = st.session_state.app_data

# --- 3. DESI FOOD DATABASE ---
food_db = {
    "paratha": {"cal": 290, "tags": ["paratha", "pratha", "porota"]},
    "anda": {"cal": 78, "tags": ["egg", "anda", "eggs", "boiled", "omelette"]},
    "biryani": {"cal": 450, "tags": ["biryani", "pulao", "rice", "chawal"]},
    "roti": {"cal": 110, "tags": ["roti", "chapati", "phulka", "naan"]},
    "daal": {"cal": 180, "tags": ["daal", "dal", "lentils", "haleem"]},
    "chicken": {"cal": 300, "tags": ["chicken", "murghi", "tikka", "karahi"]},
    "chai": {"cal": 90, "tags": ["chai", "tea", "doodh patti"]},
    "fruit": {"cal": 80, "tags": ["fruit", "apple", "banana", "kela", "aam"]},
    "nihari": {"cal": 500, "tags": ["nihari", "neheri"]},
    "samosa": {"cal": 250, "tags": ["samosa", "pakora", "shami"]}
}

# --- 4. MAIN INTERFACE ---
st.title("🥗 Sehat28")
st.markdown("*Badlo Apni Sehat, Badlo Apni Zindagi*")

# STEP 1: Profile Setup
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
            # Target Calculation
            target = (10*u_weight + 6.25*u_height - 5*u_age + 5) * 1.2
            db["profile"] = {
                "target": int(target - 500 if u_goal == "Weight Loss" else target + 500),
                "goal": u_goal
            }
            save_all_data(db)
            st.rerun()

# STEP 2: Dashboard
else:
    day = db["current_day"]
    day_key = f"day_{day}"
    
    if day_key not in db["days_log"]:
        db["days_log"][day_key] = {"cal": 0, "water": 0, "meals": []}

    # Header Card
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e2130 0%, #2b2f48 100%); padding: 25px; border-radius: 15px; border: 1px solid #4CAF50; color: white; text-align: center; margin-bottom: 20px;">
            <h1 style="margin:0;">🏆 Day {day} of 28</h1>
            <p style="margin:5px; color:#4CAF50;"><b>Goal: {db['profile']['goal']} | Target: {db['profile']['target']} kcal</b></p>
        </div>
    """, unsafe_allow_html=True)

    col_meal, col_water = st.columns(2)
    
    with col_meal:
        st.subheader("🍽️ Meal Tracker")
        query = st.text_input("Aap ne kya khaya?", placeholder="e.g. 2 anda aur 1 roti", key="food_q").lower()
        if query:
            found = False
            for item, info in food_db.items():
                for tag in info["tags"]:
                    if tag in query:
                        found = True
                        num = re.search(r'(\d+)', query)
                        qty = int(num.group(1)) if num else 1
                        total_cal = info['cal'] * qty
                        if st.button(f"Add {qty} {item.capitalize()} (+{total_cal} kcal)", use_container_width=True):
                            db["days_log"][day_key]["cal"] += total_cal
                            save_all_data(db)
                            st.success("Added!")
                            st.rerun()
            if not found and query != "":
                st.warning("Ye dish hamari dictionary mein nahi hai.")

    with col_water:
        st.subheader("💧 Water Tracker")
        glasses = db["days_log"][day_key]["water"]
        st.markdown(f"**{glasses} / 12** Glasses Today")
        if st.button("➕ Add 1 Glass Water", use_container_width=True):
            db["days_log"][day_key]["water"] += 1
            save_all_data(db)
            st.rerun()

    st.divider()

    # Progress Area
    st.subheader("📊 Today's Progress")
    curr_cal = db["days_log"][day_key]["cal"]
    t_cal = db["profile"]["target"]
    
    c1, c2 = st.columns(2)
    c1.metric("Calories", f"{curr_cal} / {t_cal} kcal")
    c1.progress(min(curr_cal / t_cal, 1.0))
    
    c2.metric("Water", f"{glasses} / 12 Glasses")
    c2.progress(min(glasses / 12, 1.0))

    st.write("")
    if st.button("🏁 FINISH DAY & SAVE PROGRESS", use_container_width=True):
        if day < 28:
            db["current_day"] += 1
            save_all_data(db)
            st.balloons()
            st.rerun()
        else:
            st.success("🎉 MUBARAK HO! 28-Day Challenge Completed!")

    # Reset Option
    with st.expander("⚙️ Settings"):
        if st.button("Reset Everything"):
            if os.path.exists(DATA_FILE): os.remove(DATA_FILE)
            st.session_state.app_data = {"profile": {}, "days_log": {}, "current_day": 1}
            st.rerun()

# --- FOOTER ---
st.divider()
st.markdown("<p style='text-align: center; color: #888;'>Developed by Abbas Ali | Sehat28 V1.0 Stable</p>", unsafe_allow_html=True)
