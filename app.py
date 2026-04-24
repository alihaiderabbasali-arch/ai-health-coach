import streamlit as st
from datetime import date

# 1. Page Configuration
st.set_page_config(page_title="AI Health Coach PRO", page_icon="👨‍⚕️", layout="centered")

# 2. Advanced Styling (Animations, Red Flags, Professional Medical UI)
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

# --- SYSTEM MEMORY (For Interconnection) ---
if 'daily_cal' not in st.session_state: st.session_state.daily_cal = 0
if 'daily_pro' not in st.session_state: st.session_state.daily_pro = 0

# --- SIDEBAR: The Live Dashboard ---
with st.sidebar:
    st.header("🏁 28-Day Challenge")
    goal = st.selectbox("Apna Goal Chunain:", ["Weight Loss", "Weight Gain", "Muscle Building"])
    target_kg = st.number_input("Target (kg)", 1, 20, 5)
    
    # Calculation: Calories limit based on Goal
    limit = 1600 if goal == "Weight Loss" else 2800
    
    st.markdown("---")
    st.subheader("📊 Today's Progress")
    st.metric("Calories Eaten", f"{st.session_state.daily_cal} kcal")
    st.metric("Protein Intake", f"{st.session_state.daily_pro}g")
    
    rem = limit - st.session_state.daily_cal
    st.write(f"**Remaining:** {rem} kcal")
    st.progress(min(st.session_state.daily_cal / limit, 1.0))
    
    if st.button("Reset Today's Stats"):
        st.session_state.daily_cal = 0
        st.session_state.daily_pro = 0
        st.rerun()

# --- MAIN APP ---
st.title("👨‍⚕️ Pro AI Health Engine")
st.write(f"Goal: **{goal}** | Challenge Day: {date.today().day % 28}")

# --- THE MEGA DESI DICTIONARY (Multi-Language & Expert Data) ---
food_db = {
    "paratha": {
        "tags": ["paratha", "pratha", "porota", "parontha", "pountha", "desi ghee roti", "fried bread"],
        "cal": 290, "pro": 6, "fat": 15, "carb": 42, "min": "Iron, Sodium", "type": "bad",
        "doc": "Senior Doctor: High saturated fats and trans-fats detected. Switch to Multigrain Roti for heart health."
    },
    "egg": {
        "tags": ["egg", "anda", "anday", "dim", "baida", "omelette", "amlet", "half fry", "ubla anda", "boiled egg"],
        "cal": 78, "pro": 7, "fat": 5, "carb": 0.6, "min": "Zinc, Vitamin D, B12", "type": "good",
        "doc": "Clinical Advice: Pure protein source (Albumin). Excellent for muscle repair during 28-day challenge."
    },
    "biryani": {
        "tags": ["biryani", "briyani", "rice", "chawal", "pulao", "polao", "tahari", "mutton rice", "chicken rice"],
        "cal": 480, "pro": 18, "fat": 22, "carb": 65, "min": "Sodium, Potassium", "type": "bad",
        "doc": "Specialist Warning: High calorie density and sodium retention risk. Avoid eating at night."
    },
    "chai": {
        "tags": ["chai", "tea", "tea", "doodh patti", "mix chai", "karak", "pink tea", "shai", "green tea", "kahwa", "cup of tea"],
        "cal": 90, "pro": 2, "fat": 3, "carb": 12, "min": "Magnesium, Antioxidants", "type": "neutral",
        "doc": "Doctor's Advice: Limit sugar. Excessive tea inhibits calcium and iron absorption. 1 hour gap needed."
    },
    "roti": {
        "tags": ["roti", "chapati", "phulka", "bread", "nan", "naan", "kulcha", "khamiri", "tandoori"],
        "cal": 120, "pro": 4, "fat": 0.5, "carb": 26, "min": "Fiber, Magnesium", "type": "good",
        "doc": "Medical Tip: Whole wheat roti fiber is essential for insulin control and smooth digestion."
    },
    "chicken grill": {
        "tags": ["chicken", "tikka", "grill", "murghi", "karahi", "roasted chicken", "murgi"],
        "cal": 230, "pro": 31, "fat": 4, "carb": 0, "min": "B6, Zinc, Phosphorus", "type": "good",
        "doc": "Expert Choice: The gold standard for fat loss. Lean meat burns fat while building muscle."
    },
    "daal": {
        "tags": ["daal", "dal", "lentils", "dhal", "tadka dal", "shorba", "chanay", "lobia"],
        "cal": 180, "pro": 9, "fat": 2, "carb": 30, "min": "Folate, Fiber", "type": "good",
        "doc": "Nutritionist Note: Plant-based protein with high fiber. Keeps metabolic rate stable."
    }
}

# --- SEARCH INTERFACE ---
user_input = st.text_input("Aapne aaj kya khaya?", placeholder="Maslan: Maine 2 anday aur 1 cup chai pi...").lower()

if user_input:
    matched = False
    for meal_key, info in food_db.items():
        # Smart detection of keywords in a full sentence
        if any(tag in user_input for tag in info["tags"]):
            matched = True
            st.markdown(f"""
            <div class="report-container">
                <h2 style="color:#4CAF50;">📋 Analysis: {meal_key.upper()}</h2>
                <div class="data-line">🔥 Calories: <span class="value">{info['cal']} kcal</span></div>
                <div class="data-line">💪 Protein: <span class="value">{info['pro']}g</span></div>
                <div class="data-line">🍔 Total Fats: <span class="value">{info['fat']}g</span></div>
                <div class="data-line">🍞 Carbohydrates: <span class="value">{info['carb']}g</span></div>
                <div class="data-line">🧪 Minerals: <span class="value">{info['min']}</span></div>
            """)

            # RED FLAG LOGIC
            if goal == "Weight Loss" and info['type'] == "bad":
                st.markdown('<div class="red-flag">🚩 RED FLAG: Yeh aapke Weight Loss goal ke khilaf hai!</div>', unsafe_allow_html=True)
            elif goal == "Weight Gain" and meal_key == "daal":
                st.markdown('<div class="red-
