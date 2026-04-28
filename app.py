import streamlit as st
import pandas as pd
import re
import json
import os

# --- 1. CONFIG ---
st.set_page_config(page_title="Sehat28 Pro", page_icon="🥗", layout="centered")

DATA_FILE = "sehat28_master_data.json"

# --- 2. STORAGE ENGINE ---
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                if "history" not in data: data["history"] = {}
                if "current_day" not in data: data["current_day"] = 1
                return data
        except: return {"profile": {}, "current_day": 1, "history": {}}
    return {"profile": {}, "current_day": 1, "history": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

if 'app_data' not in st.session_state:
    st.session_state.app_data = load_data()

db = st.session_state.app_data

# --- 3. DICTIONARY (Good/Bad/Heavy) ---
master_food_db = {
    "Roti/Chapati": {"tags": ["roti", "chapati", "phulka", "nan", "naan"], "vals": [110, 3, 22, 1, 2], "type": "good"},
    "Paratha": {"tags": ["paratha", "pratha", "porota"], "vals": [290, 6, 35, 14, 1], "type": "heavy"},
    "Rice/Biryani": {"tags": ["rice", "chawal", "biryani", "pulao"], "vals": [400, 12, 55, 15, 2], "type": "heavy"},
    "Salad/Sabzi": {"tags": ["sabzi", "tarkari", "salad", "palak", "bhindi"], "vals": [120, 4, 15, 2, 12], "type": "good"},
    "Daal/Lentils": {"tags": ["daal", "dal", "haleem", "chana"], "vals": [180, 10, 25, 4, 5], "type": "good"},
    "Chicken/Meat": {"tags": ["chicken", "murghi", "meat", "beef", "mutton", "tikka"], "vals": [300, 25, 2, 18, 3], "type": "good"},
    "Egg/Anda": {"tags": ["egg", "anda", "omlet"], "vals": [78, 7, 1, 5, 4], "type": "good"},
    "Chai/Tea": {"tags": ["chai", "tea", "doodh patti"], "vals": [90, 2, 12, 4, 1], "type": "neutral"},
    "Samosa/Snacks": {"tags": ["samosa", "pakora", "shami", "roll", "junk", "burger", "pizza"], "vals": [350, 5, 40, 25, 0], "type": "bad"},
    "Fruits": {"tags": ["fruit", "apple", "kela", "banana", "aam"], "vals": [90, 1, 23, 0, 10], "type": "good"},
    "Milk/Doodh": {"tags": ["milk", "doodh", "yogurt"], "vals": [150, 8, 12, 8, 8], "type": "good"}
}

# --- 4. LOGIC ---
def process_diet(text):
    total = [0, 0, 0, 0, 0]
    items_added = []
    bad_count = 0
    text = text.lower()
    for name, info in master_food_db.items():
        for tag in info["tags"]:
            if tag in text:
                match = re.search(rf'(\d+)\s*{tag}|{tag}\s*(\d+)', text)
                qty = int(match.group(1) or match.group(2)) if match else 1
                for i in range(5): total[i] += info["vals"][i] * qty
                items_added.append(f"{qty} {name}")
                if info["type"] == "bad": bad_count += qty
                break
    return total, items_added, bad_count

# --- 5. UI ---
st.title("🥗 Sehat28 Pro")

# --- PROFILE SECTION (With Edit Feature) ---
if not db.get("profile"):
    st.subheader("👋 Setup Your Profile")
    w = st.number_input("Weight (kg)", 40, 150, 70)
    h = st.number_input("Height (cm)", 120, 220, 170)
    a = st.number_input("Age", 15, 80, 25)
    g = st.selectbox("Goal", ["Weight Loss", "Muscle Gain"])
    
    if st.button("🚀 Start Challenge", use_container_width=True):
        bmr = (10*w + 6.25*h - 5*a + 5) * 1.2
        db["profile"] = {"w": w, "h": h, "a": a, "g": g, "target": int(bmr-500 if g=="Weight Loss" else bmr+500), "bmr": int(bmr)}
        save_data(db)
        st.rerun()
else:
    # Sidebar or Expander for Editing Profile
    with st.sidebar:
        st.header("⚙️ Profile Settings")
        curr = db["profile"]
        new_w = st.number_input("Weight (kg)", 40, 150, int(curr["w"]))
        new_h = st.number_input("Height (cm)", 120, 220, int(curr["h"]))
        new_a = st.number_input("Age", 15, 80, int(curr["a"]))
        new_g = st.selectbox("Goal", ["Weight Loss", "Muscle Gain"], index=0 if curr["g"]=="Weight Loss" else 1)
        
        if st.button("Update Profile"):
            new_bmr = (10*new_w + 6.25*new_h - 5*new_a + 5) * 1.2
            db["profile"] = {"w": new_w, "h": new_h, "a": new_a, "g": new_g, "target": int(new_bmr-500 if new_g=="Weight Loss" else new_bmr+500), "bmr": int(new_bmr)}
            save_data(db)
            st.success("Profile Updated!")
            st.rerun()

    day = db["current_day"]
    day_key = f"day_{day}"
    if day_key not in db["history"]:
        db["history"][day_key] = {"cal": 0, "pro": 0, "carb": 0, "fat": 0, "vit": 0, "water": 0, "bad_items": 0}

    st.markdown(f"### 🏆 Day {day} / 28")

    # --- INPUT ---
    food_query = st.text_input("Aap ne kya khaya?", placeholder="e.g. 2 roti, 1 anda")
    if st.button("➕ Add Meal", use_container_width=True, type="primary"):
        if food_query:
            res, items, bads = process_diet(food_query)
            if items:
                db["history"][day_key]["cal"] += res[0]
                db["history"][day_key]["pro"] += res[1]
                db["history"][day_key]["carb"] += res[2]
                db["history"][day_key]["fat"] += res[3]
                db["history"][day_key]["vit"] += res[4]
                db["history"][day_key]["bad_items"] += bads
                save_data(db)
                st.rerun()

    if st.button("💧 Add Water", use_container_width=True):
        db["history"][day_key]["water"] += 1
        save_data(db)
        st.rerun()

    st.divider()

    # --- STATUS & CALCS ---
    s = db["history"][day_key]
    bmr = db["profile"]["bmr"]
    weight_impact = ((s['cal'] - bmr) / 7700) * 1000

    # 🚩 RED FLAGS
    if s['bad_items'] > 1 or s['cal'] > db['profile']['target'] + 200 or (s['water'] < 3 and s['cal'] > 500):
        st.error("### 🚩 RED FLAGS DETECTED!")
        if s['bad_items'] > 1: st.write("- Junk food alert! Parhez karein.")
        if s['cal'] > db['profile']['target']: st.write("- Calorie limit cross ho gayi hai.")
        if s['water'] < 5: st.write("- Pani boht kam piya hai.")

    # ⚖️ WEIGHT IMPACT
    st.write(f"🔥 **Calories:** {s['cal']} / {db['profile']['target']}")
    if weight_impact < 0:
        st.success(f"📉 Losing **{abs(round(weight_impact, 1))}g** today.")
    else:
        st.warning(f"📈 Gaining **{round(weight_impact, 1)}g** today.")

    st.divider()
    
    # 🩺 DR. ADVICE
    st.subheader("🩺 Doctor's Advice")
    if s['vit'] < 5: st.info("Advice: Vitamins barhane ke liye sabzi ya phal khayein.")
    elif s['pro'] < 40: st.info("Advice: Protein ki kami hai, anda ya daal shamil karein.")
    elif s['bad_items'] > 0: st.warning("Advice: Junk food cholesterol barhata hai, dhiyaan dein.")
    else: st.success("Advice: Excellent! Aapki diet bilkul sahi hai.")

    st.divider()
    st.write(f"💪 **Pro:** {s['pro']}g | 🥖 **Carb:** {s['carb']}g | 🥑 **Fat:** {s['fat']}g")
    st.write(f"💧 **Water:** {s['water']} / 12 Glasses")

    if st.button("🏁 Finish Day", use_container_width=True):
        db["current_day"] += 1
        save_data(db)
        st.balloons(); st.rerun()

st.markdown("<p style='text-align: center; color: #888;'>Sehat28 | Developed by Abbas Ali</p>", unsafe_allow_html=True)
