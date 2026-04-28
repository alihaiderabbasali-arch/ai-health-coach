import streamlit as st
import pandas as pd
import re
import json
import os

# --- 1. CONFIG ---
st.set_page_config(page_title="Sehat28", page_icon="🥗", layout="centered")

DATA_FILE = "sehat28_master_data.json"

# --- 2. STORAGE ENGINE (With Auto-Migration) ---
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

# --- 3. THE HUGE DESI DICTIONARY (India, Pakistan, Bangladesh) ---
# Format: [Calories, Protein, Carbs, Fats, Vitamins]
master_food_db = {
    "Roti/Chapati": {"tags": ["roti", "chapati", "phulka", "nan", "naan", "khamiri"], "vals": [110, 3, 22, 1, 2]},
    "Paratha": {"tags": ["paratha", "pratha", "porota", "aloo paratha"], "vals": [290, 6, 35, 14, 1]},
    "Rice/Biryani": {"tags": ["rice", "chawal", "biryani", "pulao", "palao", "mandi"], "vals": [400, 12, 55, 15, 2]},
    "Salad/Sabzi": {"tags": ["sabzi", "tarkari", "salad", "palak", "gobi", "bhindi", "tinda", "saag", "aloo gajar"], "vals": [120, 4, 15, 2, 12]},
    "Daal/Lentils": {"tags": ["daal", "dal", "haleem", "dhal", "chana", "lobia"], "vals": [180, 10, 25, 4, 5]},
    "Chicken/Meat": {"tags": ["chicken", "murghi", "meat", "beef", "mutton", "tikka", "karahi", "korma", "kebab", "kabab"], "vals": [300, 25, 2, 18, 3]},
    "Egg/Anda": {"tags": ["egg", "anda", "omlet", "omelette", "boiled egg"], "vals": [78, 7, 1, 5, 4]},
    "Chai/Tea": {"tags": ["chai", "tea", "doodh patti", "kawa", "kahwa"], "vals": [90, 2, 12, 4, 1]},
    "Samosa/Snacks": {"tags": ["samosa", "pakora", "shami", "roll", "chaat", "gol gappa", "pani puri"], "vals": [250, 4, 25, 16, 0]},
    "Fruits": {"tags": ["fruit", "apple", "kela", "banana", "aam", "mango", "amrood", "guava", "malta", "orange"], "vals": [90, 1, 23, 0, 10]},
    "Milk/Doodh": {"tags": ["milk", "doodh", "lassi", "yogurt", "dahi"], "vals": [150, 8, 12, 8, 8]},
    "Fish": {"tags": ["fish", "machli", "machli fry"], "vals": [200, 22, 0, 10, 6]}
}

# --- 4. SMART SEARCH LOGIC ---
def calculate_nutrition(user_input):
    total = [0, 0, 0, 0, 0]
    found_items = []
    text = user_input.lower()
    
    for name, info in master_food_db.items():
        for tag in info["tags"]:
            if tag in text:
                # Qty dhoondne ki koshish (e.g., "2 roti" or "roti 2")
                match = re.search(rf'(\d+)\s*{tag}|{tag}\s*(\d+)', text)
                qty = 1
                if match:
                    qty = int(match.group(1) or match.group(2))
                
                for i in range(5):
                    total[i] += info["vals"][i] * qty
                found_items.append(f"{qty} {name}")
                break # Ek category ke liye ek hi tag kafi hai
    return total, found_items

# --- 5. MAIN UI ---
st.title("🥗 Sehat28")
st.markdown("*Apki Sehat, Apki Zubaan Mein*")

if not db.get("profile"):
    st.subheader("👋 Profile Setup")
    c1, c2 = st.columns(2)
    with c1:
        w = st.number_input("Weight (kg)", 40, 150, 70)
        h = st.number_input("Height (cm)", 120, 220, 170)
    with c2:
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
    if day_key not in db["history"]:
        db["history"][day_key] = {"cal": 0, "pro": 0, "carb": 0, "fat": 0, "vit": 0, "water": 0}

    st.markdown(f"### 🏆 Day {day} / 28")

    # --- INPUT SECTION ---
    query = st.text_input("Aap ne kya khaya?", placeholder="e.g. 2 roti aur murghi karahi")
    
    col_a, col_b = st.columns(2)
    if col_a.button("➕ Add Food", use_container_width=True):
        if query:
            results, items = calculate_nutrition(query)
            if items:
                db["history"][day_key]["cal"] += results[0]
                db["history"][day_key]["pro"] += results[1]
                db["history"][day_key]["carb"] += results[2]
                db["history"][day_key]["fat"] += results[3]
                db["history"][day_key]["vit"] += results[4]
                save_data(db)
                st.success(f"Added: {', '.join(items)}")
                st.rerun()
            else:
                st.warning("Sorry! Ye hamari desi list mein nahi hai. Kuch aur try karein?")

    if col_b.button("💧 Add Water", use_container_width=True):
        db["history"][day_key]["water"] += 1
        save_data(db)
        st.rerun()

    st.divider()

    # --- LINEAR STATUS ---
    s = db["history"][day_key]
    t = db["profile"]["target"]
    
    st.write(f"🔥 **Calories:** {s['cal']} / {t} kcal")
    st.progress(min(s['cal']/t, 1.0) if t > 0 else 0)
    st.write(f"💪 **Protein:** {s['pro']}g | 🥖 **Carbs:** {s['carb']}g")
    st.write(f"🥑 **Fats:** {s['fat']}g | ✨ **Vitamins:** {s['vit']} pts")
    st.write(f"💧 **Water:** {s['water']} / 12 Glasses")

    st.divider()

    if st.button("🏁 Finish Day", use_container_width=True):
        if day < 28:
            db["current_day"] += 1
            save_data(db)
            st.balloons()
            st.rerun()

    with st.expander("📜 History & Settings"):
        if db["history"]:
            st.table(pd.DataFrame.from_dict(db['history'], orient='index'))
        if st.button("Reset Everything"):
            if os.path.exists(DATA_FILE): os.remove(DATA_FILE)
            st.session_state.app_data = {"profile": {}, "current_day": 1, "history": {}}
            st.rerun()

st.markdown("<p style='text-align: center; color: #888; font-size: 0.8em;'>Developed by Abbas Ali | Sehat28 V1.0 Stable</p>", unsafe_allow_html=True)
