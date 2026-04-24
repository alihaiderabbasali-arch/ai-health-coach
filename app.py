import streamlit as st
from datetime import date

# 1. Page Configuration
st.set_page_config(page_title="AI Health Coach PRO", page_icon="👨‍⚕️", layout="centered")

# 2. Advanced CSS (Clean & Fixed Design)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .report-container { 
        background-color: #1e2130; padding: 20px; border-radius: 15px; 
        border-left: 5px solid #4CAF50; margin-bottom: 20px; color: white;
    }
    .data-line { font-size: 1.1em; margin-bottom: 8px; border-bottom: 1px solid #333; padding-bottom: 5px; }
    .value { color: #4CAF50; font-weight: bold; float: right; }
    .red-flag {
        background-color: rgba(255, 0, 0, 0.2); padding: 15px; 
        border-radius: 10px; border: 2px solid #ff4b4b; margin-top: 15px;
        color: #ff4b4b; font-weight: bold; animation: blinker 1.5s linear infinite;
    }
    @keyframes blinker { 50% { opacity: 0.5; } }
    .doctor-advice { 
        background-color: rgba(255, 204, 0, 0.1); padding: 15px; 
        border-radius: 10px; border: 1px solid #ffcc00; margin-top: 15px; color: #ddd;
    }
    .medical-tag { color: #ffcc00; font-weight: bold; font-size: 1.1em; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# --- APP LOGIC / SESSION STATE ---
if 'daily_cal' not in st.session_state: st.session_state.daily_cal = 0
if 'daily_pro' not in st.session_state: st.session_state.daily_pro = 0

# --- SIDEBAR (Interconnected 28-Day Dashboard) ---
with st.sidebar:
    st.header("🏁 28-Day Tracker")
    user_goal = st.selectbox("Select Your Goal:", ["Weight Loss", "Weight Gain", "Muscle Building"])
    weight_target = st.number_input("Target (kg)", 1, 20, 5)
    
    daily_limit = 1600 if user_goal == "Weight Loss" else 2800
    
    st.markdown("---")
    st.subheader("📊 Today's Progress")
    st.metric("Total Calories", f"{st.session_state.daily_cal} kcal")
    st.metric("Protein Intake", f"{st.session_state.daily_pro}g")
    
    remaining = daily_limit - st.session_state.daily_cal
    st.write(f"**Remaining:** {max(0, remaining)} kcal")
    st.progress(min(st.session_state.daily_cal / daily_limit, 1.0))
    
    if st.button("Reset Stats"):
        st.session_state.daily_cal = 0
        st.session_state.daily_pro = 0
        st.rerun()

# --- MAIN APP ---
st.title("👨‍⚕️ Global Desi Health AI")
st.write(f"Goal: **{user_goal}** | Challenge Day: **{date.today().day % 28}**")

# --- MASTER DATABASE (Desi + Global) ---
food_db = {
    "paratha": {
        "tags": ["paratha", "pratha", "porota", "parontha", "pountha", "desi ghee roti", "fried bread"],
        "cal": 290, "pro": 6, "fat": 15, "carb": 42, "min": "Iron, Sodium", "type": "bad",
        "doc": "Medical Warning: High saturated fats. Switch to Multigrain Roti for better heart health."
    },
    "egg": {
        "tags": ["egg", "anda", "anday", "dim", "baida", "omelette", "amlet", "half fry", "boiled egg", "ubla anda"],
        "cal": 78, "pro": 7, "fat": 5, "carb": 0.6, "min": "Zinc, Vitamin D, B12", "type": "good",
        "doc": "Clinical Advice: Pure protein source. 2 boiled eggs are highly recommended for muscle recovery."
    },
    "chai": {
        "tags": ["chai", "tea", "doodh patti", "mix chai", "karak", "pink tea", "cup of tea", "shai", "coffee"],
        "cal": 90, "pro": 2, "fat": 3, "carb": 12, "min": "Magnesium, Antioxidants", "type": "neutral",
        "doc": "Specialist Note: Limit sugar. Excessive tea inhibits calcium absorption. Keep a 1-hour gap from meals."
    },
    "biryani": {
        "tags": ["biryani", "briyani", "rice", "chawal", "pulao", "polao", "tahari", "chicken rice", "mutton rice"],
        "cal": 480, "pro": 18, "fat": 22, "carb": 65, "min": "Sodium, Potassium", "type": "bad",
        "doc": "Doctor's Warning: High sodium retention risk. Avoid eating this at night during your challenge."
    },
    "roti": {
        "tags": ["roti", "chapati", "phulka", "bread", "phulki", "khamiri", "naan", "tandoori"],
        "cal": 120, "pro": 4, "fat": 0.5, "carb": 26, "min": "Fiber, Magnesium", "type": "good",
        "doc": "Doctor's Advice: Whole wheat roti fiber is great for insulin control and keeping you full."
    },
    "chicken grill": {
        "tags": ["chicken", "tikka", "grill", "murghi", "karahi", "roasted chicken", "murgi", "kebab", "kabab"],
        "cal": 230, "pro": 31, "fat": 4, "carb": 0, "min": "B6, Zinc, Phosphorus", "type": "good",
        "doc": "Expert Choice: The gold standard for fat loss and muscle building. Highly recommended."
    },
    "daal": {
        "tags": ["daal", "dal", "lentils", "dhal", "tadka dal", "chanay", "lobia", "shorba"],
        "cal": 180, "pro": 9, "fat": 2, "carb": 30, "min": "Plant protein, Fiber", "type": "good",
        "doc": "Nutritionist: High fiber helps digestion. A very healthy desi option for any goal."
    },
    "apple": {
        "tags": ["apple", "seb", "fruit", "phal", "aple"],
        "cal": 52, "pro": 0.3, "fat": 0.2, "carb": 14, "min": "Vitamin C, Fiber", "type": "good",
        "doc": "Medical Fact: High pectin fiber helps lower cholesterol. Ideal snack for weight loss."
    }
}

# --- SEARCH & UI LOGIC ---
query = st.text_input("Aapne aaj kya khaya?", placeholder="Maslan: Maine ek cup chai pi aur anda khaya...").lower()

if query:
    found_any = False
    for meal_key, data in food_db.items():
        if any(tag in query for tag in data["tags"]):
            found_any = True
            
            # 🎨 HTML DESIGN BUILDING
            report_html = f"""
            <div class="report-container">
                <h2 style="color:#4CAF50;">📋 Analysis: {meal_key.upper()}</h2>
                <div class="data-line">🔥 Calories: <span class="value">{data['cal']} kcal</span></div>
                <div class="data-line">💪 Protein: <span class="value">{data['pro']}g</span></div>
                <div class="data-line">🍔 Total Fats: <span class="value">{data['fat']}g</span></div>
                <div class="data-line">🍞 Carbohydrates: <span class="value">{data['carb']}g</span></div>
                <div class="data-line">🧪 Minerals: <span class="value">{data['min']}</span></div>
            """

            if user_goal == "Weight Loss" and data['type'] == "bad":
                report_html += '<div class="red-flag">🚩 RED FLAG: Yeh aapke Weight Loss goal ke khilaf hai!</div>'
            elif user_goal == "Weight Gain" and meal_key == "apple":
                report_html += '<div class="red-flag">🚩 NOTE: Weight Gain ke liye sirf phal kafi nahi!</div>'

            report_html += f"""
                <div class="doctor-advice">
                    <span class="medical-tag">👨‍⚕️ SENIOR DOCTOR'S ADVICE:</span><br>
                    <p style="margin-top:10px;">{data['doc']}</p>
                </div>
            </div>
            """
            
            # RENDER DESIGN
            st.markdown(report_html, unsafe_allow_html=True)
            
            # ACTION BUTTON
            if st.button(f"Add {meal_key.capitalize()} to Progress"):
                st.session_state.daily_cal += data['cal']
                st.session_state.daily_pro += data['pro']
                st.rerun()
            break

    if not found_any:
        st.info("🤖 AI is scanning... Hum jald hi is desi naam ko database mein add kar denge!")

st.divider()
st.caption("Developed by Abbas Ali | Everything Integrated Final V15.0")
