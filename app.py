import streamlit as st
from datetime import date
import pandas as pd
import re
import json
import os

# --- 1. CONFIG & STYLING ---
st.set_page_config(page_title="Gemini 28-Day Ultra", page_icon="🏆", layout="wide")
DATA_FILE = "ultra_challenge_data.json"

st.markdown("""
    <style>
    .challenge-card { background: linear-gradient(135deg, #1e2130 0%, #2b2f48 100%); padding: 20px; border-radius: 15px; border: 1px solid #4CAF50; color: white; text-align: center; }
    .stat-box { background: #11141e; padding: 10px; border-radius: 10px; border: 1px solid #333; margin: 5px; text-align: center; }
    .water-btn { background-color: #2196F3; color: white; border-radius: 50%; width: 50px; height: 50px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. STORAGE SYSTEM ---
def load_all_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f: return json.load(f)
    return {"profile": {}, "days_log": {}, "current_day": 1}

def save_all_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

if 'pro_data' not in st.session_state:
    st.session_state.pro_data = load_all_data()

db = st.session_state.pro_data

# --- 3. FOOD DICTIONARY (Desi Integrated) ---
food_db = {
    "paratha": {"cal": 290, "tags": ["paratha", "pratha"]},
    "anda": {"cal": 78, "tags": ["egg", "anda", "eggs"]},
    "biryani": {"cal": 450, "tags": ["biryani", "pulao", "rice", "chawal"]},
    "roti": {"cal": 110, "tags": ["roti", "chapati"]},
    "daal": {"cal": 180, "tags": ["daal", "dal"]},
    "chicken": {"cal": 300, "tags": ["chicken", "murghi", "tikka"]},
    "chai": {"cal": 90, "tags": ["chai", "tea"]},
    "fruit": {"cal": 80, "tags": ["fruit", "apple", "banana", "kela"]}
}

# --- 4. SIDEBAR & PROFILE ---
with st.sidebar:
    st.title("👤 Health Profile")
    if not db["profile"]:
        with st.form("p_form"):
            weight = st.number_input("Weight (kg)", 40, 150, 70)
            height = st.number_input("Height (cm)", 120, 220, 170)
            age = st.number_input("Age", 15, 80, 25)
            goal = st.selectbox("Goal", ["Weight Loss", "Muscle Gain"])
            if st.form_submit_button("Start 28-Day Challenge"):
                # Simplified Target Calculation
                target = (10*weight + 6.25*height - 5*age + 5) * 1.2
                db["profile"] = {"target": int(target - 500 if goal == "Weight Loss" else target + 500), "goal": goal}
                save_all_data(db)
                st.rerun()
    else:
        st.success(f"Goal: {db['profile']['goal']}")
        st.metric("Daily Target", f"{db['profile']['target']} kcal")
        if st.button("Reset All Data"):
            st.session_state.pro_data = {"profile": {}, "days_log": {}, "current_day": 1}
            save_all_data(st.session_state.pro_data)
            st.rerun()

# --- 5. MAIN DASHBOARD ---
if not db["profile"]:
    st.warning("👈 Please set up your profile in the sidebar first!")
else:
    # Top Challenge Header
    day = db["current_day"]
    st.markdown(f"""<div class="challenge-card"><h1>🏆 Day {day} of 28</h1><p>Consistency is the key to success!</p></div>""", unsafe_allow_html=True)
    
    # Progress Data for Today
    day_key = f"day_{day}"
    if day_key not in db["days_log"]:
        db["days_log"][day_key] = {"cal": 0, "water": 0, "meals": []}

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🍽️ Meal Tracker")
        query = st.text_input("Aap ne kya khaya?", key="food_in").lower()
        if query:
            for item, info in food_db.items():
                for tag in info["tags"]:
                    if tag in query:
                        num = re.search(r'(\d+)', query)
                        qty = int(num.group(1)) if num else 1
                        total_cal = info['cal'] * qty
                        if st.button(f"Add {qty} {item} ({total_cal} kcal)"):
                            db["days_log"][day_key]["cal"] += total_cal
                            db["days_log"][day_key]["meals"].append(f"{qty} {item}")
                            save_all_data(db)
                            st.rerun()

    with col2:
        st.subheader("💧 Water Intake")
        c_water = db["days_log"][day_key]["water"]
        st.write(f"Glasses Drunk: **{c_water}** / 12")
        if st.button("➕ Add 1 Glass Water"):
            db["days_log"][day_key]["water"] += 1
            save_all_data(db)
            st.rerun()

    st.divider()

    # Integrated Stats
    c1, c2, c3 = st.columns(3)
    today_cal = db["days_log"][day_key]["cal"]
    target_cal = db["profile"]["target"]
    
    with c1:
        st.metric("Calories Consumed", f"{today_cal} kcal")
        st.progress(min(today_cal / target_cal, 1.0))
    with c2:
        water_pct = min(c_water / 12, 1.0)
        st.metric("Hydration Status", f"{int(water_pct*100)}%")
        st.progress(water_pct)
    with c3:
        if st.button("🏁 COMPLETE DAY & MOVE NEXT"):
            if day < 28:
                db["current_day"] += 1
                save_all_data(db)
                st.success(f"Day {day} Completed! See you tomorrow.")
                st.rerun()
            else:
                st.balloons()
                st.success("CONGRATULATIONS! 28-Day Challenge Completed!")

    # 📈 HISTORY CHART
    st.subheader("📈 28-Day Journey Analysis")
    if db["days_log"]:
        history_df = pd.DataFrame.from_dict(db["days_log"], orient='index')
        st.line_chart(history_df[['cal', 'water']])

st.caption("Developed by Abbas Ali | Gemini Integrated V28.0 Ultra Stable")
