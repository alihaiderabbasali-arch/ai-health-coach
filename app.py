import streamlit as st
from datetime import date
import pandas as pd
import re
import json
import os

# --- 1. CONFIG ---
st.set_page_config(page_title="Sehat28", page_icon="🥗", layout="centered")

DATA_FILE = "sehat28_master_data.json"

# --- 2. STORAGE ENGINE (With Auto-Fix for KeyError) ---
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                # ERROR FIX: Agar 'history' dictionary nahi hai to bana do
                if "history" not in data:
                    data["history"] = {}
                if "current_day" not in data:
                    data["current_day"] = 1
                return data
        except:
            return {"profile": {}, "current_day": 1, "history": {}}
    return {"profile": {}, "current_day": 1, "history": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

if 'app_data' not in st.session_state:
    st.session_state.app_data = load_data()

db = st.session_state.app_data

# --- 3. NUTRITION DB ---
food_db = {
    "paratha": {"tags": ["paratha", "pratha"], "vals": [290, 6, 35, 14, 1]},
    "anda": {"tags": ["egg", "anda", "eggs"], "vals": [78, 7, 1, 5, 4]},
    "biryani": {"tags": ["biryani", "pulao", "rice"], "vals": [450, 15, 60, 18, 2]},
    "roti": {"tags": ["roti", "chapati"], "vals": [110, 3, 22, 1, 2]},
    "daal": {"tags": ["daal", "dal", "lentils"], "vals": [180, 9, 25, 4, 5]},
    "chicken": {"tags": ["chicken", "murghi", "tikka"], "vals": [300, 25, 2, 15, 3]},
    "chai": {"tags": ["chai", "tea"], "vals": [90, 2, 12, 4, 1]},
    "fruit": {"tags": ["apple", "kela", "banana", "aam"], "vals": [90, 1, 23, 0, 10]},
    "sabzi": {"tags": ["sabzi", "palak", "tarkari"], "vals": [150, 4, 15, 2, 12]},
    "doodh": {"tags": ["milk", "doodh"], "vals": [150, 8, 12, 8, 8]}
}

# --- 4. MAIN UI ---
st.title("🥗 Sehat28")
st.markdown("*Badlo Apni Sehat, Badlo Apni Zindagi*")

if not db.get("profile"):
    st.subheader("👋 Setup Your Profile")
    w = st.number_input("Weight (kg)", 40, 150, 70)
    h = st.number_input("Height (cm)", 120, 220, 170)
    a = st.number_input("Age", 15, 80, 25)
    g = st.selectbox("Goal", ["Weight Loss", "Muscle Gain"])
    if st.button("🚀 Start Challenge", use_container_width=True):
        target = (10*w + 6.25*h - 5*a + 5) * 1.2
        db["profile"] = {"target": int(target-500 if g=="Weight Loss" else target+500), "goal": g}
        save_data(db)
        st.rerun()
else:
    day = db["current_day"]
    day_key = f"day_{day}"
    
    # Check again if history exists for current day
    if day_key not in db["history"]:
        db["history"][day_key] = {"cal": 0, "pro": 0, "carb": 0, "fat": 0, "vit": 0, "water": 0}

    st.markdown(f"### 🏆 Day {day} / 28")

    # Inputs
    query = st.text_input("Aap ne kya khaya?", placeholder="e.g. 2 anda, 1 roti")
    
    col_a, col_b = st.columns(2)
    if col_a.button("➕ Add Food", use_container_width=True):
        if query:
            for item, info in food_db.items():
                for tag in info["tags"]:
                    if tag in query.lower():
                        num = re.search(r'(\d+)', query)
                        qty = int(num.group(1)) if num else 1
                        db["history"][day_key]["cal"] += info["vals"][0] * qty
                        db["history"][day_key]["pro"] += info["vals"][1] * qty
                        db["history"][day_key]["carb"] += info["vals"][2] * qty
                        db["history"][day_key]["fat"] += info["vals"][3] * qty
                        db["history"][day_key]["vit"] += info["vals"][4] * qty
            save_data(db)
            st.rerun()

    if col_b.button("💧 Add Water", use_container_width=True):
        db["history"][day_key]["water"] += 1
        save_data(db)
        st.rerun()

    st.divider()

    # Linear Status Display
    s = db["history"][day_key]
    t = db["profile"]["target"]
    
    st.write(f"🔥 **Calories:** {s['cal']} / {t} kcal")
    st.progress(min(s['cal']/t, 1.0) if t > 0 else 0)
    
    st.write(f"💪 **Protein:** {s['pro']}g")
    st.write(f"🥖 **Carbs:** {s['carb']}g")
    st.write(f"🥑 **Fats:** {s['fat']}g")
    st.write(f"✨ **Vitamins:** {s['vit']} points")
    st.write(f"💧 **Water:** {s['water']} / 12 Glasses")

    st.divider()

    if st.button("🏁 Finish Day", use_container_width=True):
        if day < 28:
            db["current_day"] += 1
            save_data(db)
            st.balloons()
            st.rerun()

    with st.expander("📜 View History & Settings"):
        if db["history"]:
            st.table(pd.DataFrame.from_dict(db['history'], orient='index'))
        if st.button("Reset All Progress"):
            if os.path.exists(DATA_FILE): os.remove(DATA_FILE)
            st.session_state.app_data = {"profile": {}, "current_day": 1, "history": {}}
            st.rerun()

st.markdown("<p style='text-align: center; color: #888; font-size: 0.8em;'>Developed by Abbas Ali | Sehat28 V1.0 Stable</p>", unsafe_allow_html=True)
