import streamlit as st
import pandas as pd
import re
import json
import os

# --- 1. CONFIG & STYLING ---
# Title se "Pro" hata diya gaya hai
st.set_page_config(page_title="Sehat28", page_icon="🥗", layout="centered")

DATA_FILE = "sehat28_master_data.json"

# --- 2. STORAGE ENGINE (With Universal Format Fix) ---
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                
                # Check 1: Structure Fix (Day 1 fix)
                if "history" not in data: data["history"] = {}
                if "current_day" not in data: data["current_day"] = 1
                
                # Check 2: Profile Format Fix (The Edit Feature Fix)
                # Agar user ne boht purane code se profile banayi thi jisme keys choti thi, use fix karo
                if "profile" in data and "w" not in data["profile"] and "Weight (kg)" in data["profile"]:
                    p = data["profile"]
                    # Calculate BMR again in old format if keys are missing
                    old_w = p["Weight (kg)"]
                    old_h = p["Height (cm)"]
                    old_a = p["Age"]
                    old_g = p["Goal"]
                    new_bmr = (10*old_w + 6.25*old_h - 5*old_a + 5) * 1.2
                    
                    data["profile"] = {
                        "w": old_w, "h": old_h, "a": old_a, "g": old_g,
                        "target": p.get("Target Calories", int(new_bmr-500 if old_g=="Weight Loss" else new_bmr+500)),
                        "bmr": int(new_bmr)
                    }
                
                return data
        except: return {"profile": {}, "current_day": 1, "history": {}}
    return {"profile": {}, "current_day": 1, "history": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

if 'app_data' not in st.session_state:
    st.session_state.app_data = load_data()

db = st.session_state.app_data

# --- 3. UPDATED DICTIONARY (Good/Bad/Heavy) ---
master_food_db = {
    "Roti/Chapati": {"tags": ["roti", "chapati", "phulka", "nan", "naan", "khamiri"], "vals": [110, 3, 22, 1, 2], "type": "good"},
    "Paratha": {"tags": ["paratha", "pratha", "porota", "aloo paratha"], "vals": [290, 6, 35, 14, 1], "type": "heavy"},
    "Rice/Biryani": {"tags": ["rice", "chawal", "biryani", "pulao", "palao", "mandi"], "vals": [400, 12, 55, 15, 2], "type": "heavy"},
    "Salad/Sabzi": {"tags": ["sabzi", "tarkari", "salad", "palak", "gobi", "bhindi", "saag"], "vals": [120, 4, 15, 2, 12], "type": "good"},
    "Daal/Lentils": {"tags": ["daal", "dal", "haleem", "chana", "lobia"], "vals": [180, 10, 25, 4, 5], "type": "good"},
    "Chicken/Meat": {"tags": ["chicken", "murghi", "meat", "beef", "mutton", "tikka", "kebab"], "vals": [300, 25, 2, 18, 3], "type": "good"},
    "Egg/Anda": {"tags": ["egg", "anda", "omlet", "omelette"], "vals": [78, 7, 1, 5, 4], "type": "good"},
    "Chai/Tea": {"tags": ["chai", "tea", "doodh patti"], "vals": [90, 2, 12, 4, 1], "type": "neutral"},
    "Samosa/Snacks": {"tags": ["samosa", "pakora", "shami", "junk", "burger", "pizza", "roll"], "vals": [350, 5, 40, 25, 0], "type": "bad"},
    "Fruits": {"tags": ["fruit", "apple", "kela", "banana", "mango", "aam"], "vals": [90, 1, 23, 0, 10], "type": "good"},
    "Milk/Doodh": {"tags": ["milk", "doodh", "yogurt", "lassi"], "vals": [150, 8, 12, 8, 8], "type": "good"}
}

# --- 4. ENGINE (Multi-Item & Qty Aware) ---
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

# --- 5. MAIN UI ---
# Title is now "Sehat28"
st.title("🥗 Sehat28")
st.markdown("*Badlo Apni Sehat, Badlo Apni Zindagi*")

if not db.get("profile"):
    st.subheader("👋 Setup Your Profile")
    w = st.number_input("Weight (kg)", 40, 150, 70)
    h = st.number_input("Height (cm)", 120, 220, 170)
    a = st.number_input("Age", 15, 80, 25)
    g = st.selectbox("Goal", ["Weight Loss", "Muscle Gain"])
    
    if st.button("🚀 Start My 28-Day Challenge", use_container_width=True):
        bmr = (10*w + 6.25*h - 5*a + 5) * 1.2
        db["profile"] = {"w": w, "h": h, "a": a, "g": g, "target": int(bmr-500 if g=="Weight Loss" else bmr+500), "bmr": int(bmr)}
        save_data(db)
        st.rerun()
else:
    # Sidebar Profile Editor
    with st.sidebar:
        st.header("⚙️ Profile Settings")
        curr = db["profile"]
        # Universal Fix for KeyError when editing: get old values safely
        default_w = int(curr.get("w", curr.get("Weight (kg)", 70)))
        default_h = int(curr.get("h", curr.get("Height (cm)", 170)))
        default_a = int(curr.get("a", curr.get("Age", 25)))
        default_g = curr.get("g", curr.get("Goal", "Weight Loss"))
        
        new_w = st.number_input("Update Weight (kg)", 40, 150, default_w)
        new_h = st.number_input("Update Height (cm)", 120, 220, default_h)
        new_a = st.number_input("Update Age", 15, 80, default_a)
        new_g = st.selectbox("Update Goal", ["Weight Loss", "Muscle Gain"], index=0 if default_g=="Weight Loss" else 1)
        
        if st.button("Save & Update Profile"):
            new_bmr = (10*new_w + 6.25*new_h - 5*new_a + 5) * 1.2
            db["profile"] = {"w": new_w, "h": new_h, "a": new_a, "g": new_g, "target": int(new_bmr-500 if new_g=="Weight Loss" else new_bmr+500), "bmr": int(new_bmr)}
            save_data(db)
            st.success("Profile Updated Successfully!")
            st.rerun()

    day = db["current_day"]
    day_key = f"day_{day}"
    if day_key not in db["history"]:
        db["history"][day_key] = {"cal": 0, "pro": 0, "carb": 0, "fat": 0, "vit": 0, "water": 0, "bad_items": 0}

    st.markdown(f"### 🏆 Day {day} / 28")

    # --- INPUT ---
    food_query = st.text_input("Aap ne kya khaya?", placeholder="e.g. 2 roti, 1 anda", key="food_box")
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

    if st.button("💧 Add Water Glass", use_container_width=True):
        db["history"][day_key]["water"] += 1
        save_data(db)
        st.rerun()

    st.divider()

    # --- STATUS & LIVE CALCULATIONS ---
    s = db["history"][day_key]
    bmr = db["profile"]["bmr"]
    weight_impact_g = ((s['cal'] - bmr) / 7700) * 1000

    # 🚩 RED FLAGS ALERTS
    if s['bad_items'] > 1 or s['cal'] > db['profile']['target'] + 200 or (s['water'] < 3 and s['cal'] > 500):
        st.error("### 🚩 SEHAT ALERT (Red Flags)")
        if s['bad_items'] > 1: st.write("- Fried/Junk food detected. Cholesterol risk!")
        if s['cal'] > db['profile']['target']: st.write("- Crossed daily calorie goal.")
        if s['water'] < 5: st.write("- Dehydration alert! Need more water.")

    # ⚖️ WEIGHT TRACKING
    st.write(f"🔥 **Calories:** {s['cal']} / {db['profile']['target']} kcal")
    if weight_impact_g < 0:
        st.success(f"📉 Good job! mathematically losing **{abs(round(weight_impact_g, 1))}g** today.")
    else:
        st.warning(f"📈 Careful! Mathematically gaining **{round(weight_impact_g, 1)}g** today.")

    st.divider()
    
    # 🩺 AI DR. ADVICE (Dynamic)
    st.subheader("🩺 AI Doctor's Advice")
    advice_found = False
    if s['vit'] < 5:
        st.info("Advice: Diet is low in vitamins. Please add vegetables, fruits, or salad.")
        advice_found = True
    if s['pro'] < 40 and not advice_found:
        st.info("Advice: Protein is low. Consider eggs, meat, lentils, or milk.")
        advice_found = True
    if s['bad_items'] > 0 and not advice_found:
        st.warning("Advice: Fried items/Junk food barhain cholesterol levels. Avoid regularly.")
        advice_found = True
    if not advice_found:
        st.success("Advice: Excellent routine! Balanced diet maintained. Keep it up!")

    st.divider()
    st.write(f"💪 **Protein:** {s['pro']}g  |  🥖 **Carbs:** {s['carb']}g | 🥑 **Fats:** {s['fat']}g")
    st.write(f"✨ **Vitamins:** {s['vit']} pts | 💧 **Water:** {s['water']} / 12 Glasses")

    if st.button("🏁 Finish Day & Progress Challenges", use_container_width=True):
        db["current_day"] += 1
        save_data(db)
        st.balloons(); st.rerun()

    with st.expander("📜 History & Complete Data Settings"):
        if db["history"]: st.table(pd.DataFrame.from_dict(db['history'], orient='index'))
        if st.button("Delete Everything & Restart Challenge"):
            if os.path.exists(DATA_FILE): os.remove(DATA_FILE)
            st.session_state.app_data = {"profile": {}, "current_day": 1, "history": {}}
            st.rerun()

st.markdown("<p style='text-align: center; color: #888;'>Developed by Abbas Ali | Sehat28 Stable</p>", unsafe_allow_html=True)
