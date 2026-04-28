import streamlit as st
import pandas as pd
import re
import json
import os

# --- 1. CONFIG ---
st.set_page_config(page_title="Sehat28", page_icon="🥗", layout="centered")

DATA_FILE = "sehat28_master_data.json"

# --- 2. THE ULTIMATE PROTECTION ENGINE ---
def load_data():
    default_structure = {"profile": {}, "current_day": 1, "history": {}}
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                
                # REPAIR LAYER 1: Structure Integrity
                if not isinstance(data, dict): data = default_structure
                if "profile" not in data: data["profile"] = {}
                if "history" not in data: data["history"] = {}
                if "current_day" not in data: data["current_day"] = 1

                # REPAIR LAYER 2: Profile Key Safety (Fixes Profile Update Error)
                p = data["profile"]
                if p:
                    # Map any possible old naming to new standard keys
                    w = p.get("w", p.get("Weight (kg)", 70))
                    h = p.get("h", p.get("Height (cm)", 170))
                    a = p.get("a", p.get("Age", 25))
                    g = p.get("g", p.get("Goal", "Weight Loss"))
                    bmr = p.get("bmr", int((10*w + 6.25*h - 5*a + 5) * 1.2))
                    target = p.get("target", int(bmr-500 if g=="Weight Loss" else bmr+500))
                    
                    data["profile"] = {"w": w, "h": h, "a": a, "g": g, "bmr": bmr, "target": target}

                # REPAIR LAYER 3: History Migration (Fixes KeyError: 'bad_items' or 'water')
                for day in data["history"]:
                    d = data["history"][day]
                    default_keys = {"cal": 0, "pro": 0, "carb": 0, "fat": 0, "vit": 0, "water": 0, "bad_items": 0}
                    for key, val in default_keys.items():
                        if key not in d: d[key] = val
                
                return data
        except Exception:
            return default_structure
    return default_structure

def save_data(data):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        st.error(f"Save Error: {e}")

# Initial Load
if 'app_data' not in st.session_state:
    st.session_state.app_data = load_data()

db = st.session_state.app_data

# --- 3. ROBUST FOOD DATABASE ---
master_food_db = {
    "Roti/Chapati": {"tags": ["roti", "chapati", "nan", "naan"], "vals": [110, 3, 22, 1, 2], "type": "good"},
    "Paratha": {"tags": ["paratha", "pratha"], "vals": [290, 6, 35, 14, 1], "type": "heavy"},
    "Rice/Biryani": {"tags": ["rice", "chawal", "biryani", "pulao"], "vals": [400, 12, 55, 15, 2], "type": "heavy"},
    "Salad/Sabzi": {"tags": ["sabzi", "salad", "tarkari", "bhindi", "palak"], "vals": [120, 4, 15, 2, 12], "type": "good"},
    "Egg/Anda": {"tags": ["egg", "anda", "omlet"], "vals": [78, 7, 1, 5, 4], "type": "good"},
    "Meat/Chicken": {"tags": ["chicken", "meat", "beef", "mutton", "tikka"], "vals": [300, 25, 2, 18, 3], "type": "good"},
    "Snacks/Junk": {"tags": ["samosa", "pakora", "burger", "pizza", "roll"], "vals": [350, 5, 40, 25, 0], "type": "bad"}
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

# --- 4. MAIN APP UI ---
st.title("🥗 Sehat28")
st.markdown("*Apki Sehat, Apki Zubaani*")

try:
    if not db.get("profile"):
        st.subheader("👋 Setup Profile")
        w = st.number_input("Weight (kg)", 40, 150, 70)
        h = st.number_input("Height (cm)", 120, 220, 170)
        a = st.number_input("Age", 15, 80, 25)
        g = st.selectbox("Goal", ["Weight Loss", "Muscle Gain"])
        
        if st.button("🚀 Start My 28-Day Challenge", use_container_width=True):
            bmr = (10*w + 6.25*h - 5*a + 5) * 1.2
            db["profile"] = {"w": w, "h": h, "a": a, "g": g, "target": int(bmr-500 if g=="Weight Loss" else bmr+500), "bmr": int(bmr)}
            save_data(db); st.rerun()
    else:
        # Sidebar Profile Update (Key-Safe)
        with st.sidebar:
            st.header("⚙️ Settings")
            p = db["profile"]
            # Hamesha .get() use karna taake KeyError na aaye
            new_w = st.number_input("Update Weight (kg)", 40, 150, int(p.get("w", 70)))
            new_h = st.number_input("Update Height (cm)", 120, 220, int(p.get("h", 170)))
            if st.button("Save Changes"):
                new_bmr = (10*new_w + 6.25*new_h - 5*p.get("a", 25) + 5) * 1.2
                db["profile"].update({
                    "w": new_w, "h": new_h, "bmr": int(new_bmr), 
                    "target": int(new_bmr-500 if p.get("g")=="Weight Loss" else new_bmr+500)
                })
                save_data(db); st.success("Updated!"); st.rerun()

        day = db.get("current_day", 1)
        day_key = f"day_{day}"
        if day_key not in db["history"]:
            db["history"][day_key] = {"cal": 0, "pro": 0, "carb": 0, "fat": 0, "vit": 0, "water": 0, "bad_items": 0}
        
        s = db["history"][day_key]
        st.subheader(f"🏆 Day {day} / 28")

        # INPUT
        query = st.text_input("Aap ne kya khaya?", key="food_input")
        if st.button("➕ Add Food", use_container_width=True, type="primary"):
            if query:
                res, items, bads = process_diet(query)
                if items:
                    s["cal"] += res[0]; s["pro"] += res[1]; s["bad_items"] += bads
                    save_data(db); st.rerun()

        if st.button("💧 Add Water", use_container_width=True):
            s["water"] += 1; save_data(db); st.rerun()

        # DASHBOARD
        st.divider()
        # Safe math calculation
        bmr_val = db["profile"].get("bmr", 2000)
        impact = ((s['cal'] - bmr_val) / 7700) * 1000
        
        st.write(f"🔥 **Calories:** {s['cal']} / {db['profile'].get('target', 2000)} kcal")
        if impact < 0: st.success(f"📉 Losing {abs(round(impact, 1))}g today")
        else: st.warning(f"📈 Gaining {round(impact, 1)}g today")

        if s.get("bad_items", 0) > 0:
            st.error("🚩 **Red Flag:** Junk food detected! Avoid for better weight management.")

        st.info(f"🩺 **Dr. Advice:** {'Looking good! Keep the momentum.' if s.get('bad_items', 0) == 0 else 'Fried food slows down metabolism. Try grilled next time.'}")

        st.divider()
        st.write(f"💪 **Pro:** {s['pro']}g | 💧 **Water:** {s['water']}/12 Glasses")

        if st.button("🏁 Finish Day", use_container_width=True):
            db["current_day"] += 1; save_data(db); st.balloons(); st.rerun()

except Exception as e:
    st.warning("⚠️ App encountered a data mismatch. Auto-repairing now...")
    # Atomic repair: Reset current day structure but keep profile
    if 'current_day' in db:
        day_key = f"day_{db['current_day']}"
        db["history"][day_key] = {"cal": 0, "pro": 0, "carb": 0, "fat": 0, "vit": 0, "water": 0, "bad_items": 0}
        save_data(db)
        st.button("Fix & Restart")

with st.expander("Reset App"):
    if st.button("Clear Everything"):
        if os.path.exists(DATA_FILE): os.remove(DATA_FILE)
        st.rerun()
