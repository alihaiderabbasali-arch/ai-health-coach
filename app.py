import streamlit as st
import pandas as pd
import re
import json
import os

# --- 1. CONFIG ---
st.set_page_config(page_title="Sehat28", page_icon="🥗", layout="centered")

DATA_FILE = "sehat28_master_data.json"

# --- 2. THE ULTIMATE REPAIR ENGINE ---
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                
                # Sab se ahem: Profile check aur repair
                if "profile" in data and data["profile"]:
                    p = data["profile"]
                    # Agar BMR missing hai toh fix karein
                    if "bmr" not in p:
                        w = p.get("w", p.get("Weight (kg)", 70))
                        h = p.get("h", p.get("Height (cm)", 170))
                        a = p.get("a", p.get("Age", 25))
                        p["bmr"] = int((10*w + 6.25*h - 5*a + 5) * 1.2)
                        p["w"], p["h"], p["a"] = w, h, a

                # Dusra ahem: History check (KeyErrors ko khatam karne ke liye)
                if "history" not in data: data["history"] = {}
                for day in data["history"]:
                    day_data = data["history"][day]
                    # Jo bhi missing key error de rahi hai, usey yahan 0 set kar dein
                    keys_to_fix = ["bad_items", "cal", "pro", "carb", "fat", "vit", "water"]
                    for k in keys_to_fix:
                        if k not in day_data: day_data[k] = 0
                
                if "current_day" not in data: data["current_day"] = 1
                return data
        except: return {"profile": {}, "current_day": 1, "history": {}}
    return {"profile": {}, "current_day": 1, "history": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

if 'app_data' not in st.session_state:
    st.session_state.app_data = load_data()

db = st.session_state.app_data

# --- 3. FOOD DATABASE ---
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
    "Fruits": {"tags": ["fruit", "apple", "kela", "banana", "aam"], "vals": [90, 1, 23, 0, 10], "type": "good"}
}

def process_diet(text):
    total, items, bads = [0]*5, [], 0
    text = text.lower()
    for name, info in master_food_db.items():
        for tag in info["tags"]:
            if tag in text:
                match = re.search(rf'(\d+)\s*{tag}|{tag}\s*(\d+)', text)
                qty = int(match.group(1) or match.group(2)) if match else 1
                for i in range(5): total[i] += info["vals"][i] * qty
                items.append(f"{qty} {name}")
                if info["type"] == "bad": bads += qty
                break
    return total, items, bads

# --- 4. MAIN INTERFACE ---
st.title("🥗 Sehat28")

if not db.get("profile"):
    st.subheader("👋 Profile Setup")
    w = st.number_input("Weight (kg)", 40, 150, 70)
    h = st.number_input("Height (cm)", 120, 220, 170)
    a = st.number_input("Age", 15, 80, 25)
    g = st.selectbox("Goal", ["Weight Loss", "Muscle Gain"])
    if st.button("🚀 Start My Challenge", use_container_width=True):
        bmr = (10*w + 6.25*h - 5*a + 5) * 1.2
        db["profile"] = {"w": w, "h": h, "a": a, "g": g, "target": int(bmr-500 if g=="Weight Loss" else bmr+500), "bmr": int(bmr)}
        save_data(db); st.rerun()
else:
    # Sidebar Profile Edit
    with st.sidebar:
        st.header("⚙️ Profile Settings")
        p = db["profile"]
        new_w = st.number_input("Weight (kg)", 40, 150, int(p.get("w", 70)))
        new_h = st.number_input("Height (cm)", 120, 220, int(p.get("h", 170)))
        if st.button("Update Profile"):
            new_bmr = (10*new_w + 6.25*new_h - 5*p["a"] + 5) * 1.2
            p.update({"w": new_w, "h": new_h, "bmr": int(new_bmr), "target": int(new_bmr-500 if p["g"]=="Weight Loss" else new_bmr+500)})
            save_data(db); st.success("Updated!"); st.rerun()

    day_key = f"day_{db['current_day']}"
    if day_key not in db["history"]:
        db["history"][day_key] = {"cal": 0, "pro": 0, "carb": 0, "fat": 0, "vit": 0, "water": 0, "bad_items": 0}
    
    s = db["history"][day_key]
    
    st.subheader(f"🏆 Day {db['current_day']} / 28")
    
    query = st.text_input("Aap ne kya khaya?")
    if st.button("➕ Add Meal", use_container_width=True, type="primary"):
        if query:
            res, items, bads = process_diet(query)
            if items:
                s["cal"] += res[0]; s["pro"] += res[1]; s["carb"] += res[2]; s["fat"] += res[3]; s["vit"] += res[4]; s["bad_items"] += bads
                save_data(db); st.rerun()

    if st.button("💧 Add Water", use_container_width=True):
        s["water"] += 1; save_data(db); st.rerun()

    # --- TRACKING DISPLAY ---
    st.divider()
    impact = ((s['cal'] - db["profile"]["bmr"]) / 7700) * 1000
    
    st.write(f"🔥 **Calories:** {s['cal']} / {db['profile']['target']} kcal")
    if impact < 0: st.success(f"📉 Losing {abs(round(impact, 1))}g today")
    else: st.warning(f"📈 Gaining {round(impact, 1)}g today")
    
    if s.get("bad_items", 0) > 0:
        st.error("🚩 **Red Flag:** Junk food detected! Avoid for better results.")
    
    st.info(f"🩺 **Dr. Advice:** {'Everything looks great!' if s.get('bad_items', 0) == 0 else 'Try to replace fried food with grilled or fresh items.'}")
    
    st.divider()
    st.write(f"💪 **Pro:** {s['pro']}g | 🥖 **Carb:** {s['carb']}g | 🥑 **Fat:** {s['fat']}g | 💧 **Water:** {s['water']}/12")

    if st.button("🏁 Finish Day", use_container_width=True):
        db["current_day"] += 1; save_data(db); st.balloons(); st.rerun()

    # Reset option agar boht hi bura phans jaye
    with st.expander("Reset"):
        if st.button("Delete Everything & Fresh Start"):
            if os.path.exists(DATA_FILE): os.remove(DATA_FILE)
            st.rerun()
