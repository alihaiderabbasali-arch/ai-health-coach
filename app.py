import streamlit as st
from datetime import date

# 1. Page Configuration
st.set_page_config(page_title="AI Health Coach PRO", page_icon="👨‍⚕️", layout="centered")

# 2. Professional CSS
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
    </style>
    """, unsafe_allow_html=True)

# --- SYSTEM MEMORY ---
if 'daily_cal' not in st.session_state: st.session_state.daily_cal = 0
if 'daily_pro' not in st.session_state: st.session_state.daily_pro = 0

# --- SIDEBAR (Interconnected Challenge) ---
with st.sidebar:
    st.header("🏁 28-Day Challenge")
    user_goal = st.selectbox("Apna Goal Chunain:", ["Weight Loss", "Weight Gain", "Muscle Building"])
    weight_target = st.number_input("Target Weight (kg)", 1, 20, 5)
    daily_limit = 1600 if user_goal == "Weight Loss" else 2800
    st.markdown("---")
    st.metric("Total Eaten Today", f"{st.session_state.daily_cal} kcal")
    st.progress(min(st.session_state.daily_cal / daily_limit, 1.0))
    if st.button("Reset Day"):
        st.session_state.daily_cal = 0
        st.session_state.daily_pro = 0
        st.rerun()

# --- MAIN APP ---
st.title("👨‍⚕️ Global Desi Health Engine")
st.write(f"Goal: **{user_goal}** | Challenge Day: {date.today().day % 28}")

# --- THE MEGA DESI DICTIONARY ---
# Ismein Punjabi, Urdu, Hindi aur English ke keywords ka mix hai
food_dictionary = {
    "paratha": {
        "tags": ["paratha", "pratha", "porota", "parontha", "pountha", "desi ghee roti", "fried bread"],
        "cal": 290, "pro": 6, "fat": 15, "type": "bad", 
        "doc": "Doctor's Advice: Paratha mein saturated fats zyada hain. Challenge mein 'Sookhi Roti' behtar hai."
    },
    "egg": {
        "tags": ["egg", "anda", "anday", "dim", "baida", "omelette", "amlet", "half fry", "ubla anda", "boiled egg"],
        "cal": 78, "pro": 7, "fat": 5, "type": "good", 
        "doc": "Senior Doctor: Anda protein ka best zariya hai. Isse muscle recovery tez hoti hai."
    },
    "chai": {
        "tags": ["chai", "tea", "tea", "doodh patti", "mix chai", "karak", "pink tea", "shai", "green tea", "kahwa"],
        "cal": 90, "pro": 2, "fat": 3, "type": "neutral", 
        "doc": "Medical Tip: Chai mein cheeni kam rakhein. Khane ke baad gap lazmi dein."
    },
    "biryani": {
        "tags": ["biryani", "briyani", "rice", "chawal", "pulao", "polao", "tahari", "mutton rice", "chicken rice"],
        "cal": 480, "pro": 18, "fat": 22, "type": "bad", 
        "doc": "Doctor's Warning: Biryani calories mein bohat heavy hai. Portion control ka khayal rakhein."
    },
    "roti": {
        "tags": ["roti", "chapati", "phulka", "bread", "nan", "naan", "kulcha", "khamiri", "tandoori"],
        "cal": 120, "pro": 4, "fat": 0.5, "type": "good", 
        "doc": "Medical Note: Whole wheat roti fiber ka behtareen source hai. Weight loss ke liye behtareen."
    },
    "daal": {
        "tags": ["daal", "dal", "lentils", "dhal", "tadka dal", "shorba", "chanay", "lobia"],
        "cal": 180, "pro": 9, "fat": 2, "type": "good", 
        "doc": "Nutritionist: Daal mein fiber aur protein dono hain. Isse pet der tak bhara rehta hai."
    },
    "meat": {
        "tags": ["gosht", "meat", "mutton", "beef", "chicken", "murghi", "tikka", "karahi", "kebab", "kabab"],
        "cal": 250, "pro": 25, "fat": 12, "type": "good", 
        "doc": "Doctor Advice: Lean meat (chicken breast/fish) muscle building ke liye gold standard hai."
    }
}

# User input field (Accepts anything)
user_input = st.text_input("Aapne kya khaya? (Urdu, Hindi, Punjabi ya English mein likhein)", placeholder="Maslan: Maine 2 anday aur paratha khaya...").lower()

if user_input:
    matched_any = False
    # Smart parsing logic
    for item, info in food_dictionary.items():
        if any(tag in user_input for tag in info["tags"]):
            matched_any = True
            st.markdown(f"""
            <div class="report-container">
                <h2 style="color:#4CAF50;">✅ {item.upper()} Detected</h2>
                <div class="data-line">🔥 Calories: <span class="value">{info['cal']} kcal</span></div>
                <div class="data-line">💪 Protein: <span class="value">{info['pro']}g</span></div>
            """)
            
            # Interconnected Red Flag Logic
            if user_goal == "Weight Loss" and info['type'] == "bad":
                st.markdown('<div class="red-flag">🚩 RED FLAG: Yeh aapke goal ke khilaf hai! Control karein.</div>', unsafe_allow_html=True)

            st.markdown(f"""
                <div class="doctor-advice">
                    <b style="color:#ffcc00;">👨‍⚕️ Specialist Advice:</b><br>{info['doc']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Add {item.capitalize()} to Progress"):
                st.session_state.daily_cal += info['cal']
                st.session_state.daily_pro += info['pro']
                st.rerun()

    if not matched_any:
        st.info("🤖 AI is analyzing... Hum is naye desi naam ko database mein add kar rahe hain!")

st.divider()
st.caption("Developed by Abbas Ali | Multi-Language Desi Dictionary V12.0")
import streamlit as st
from datetime import date

# 1. Page Configuration
st.set_page_config(page_title="AI Health Coach PRO", page_icon="👨‍⚕️", layout="centered")

# 2. Advanced CSS (Purana Layout + Naye Red Flags)
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

# --- SYSTEM MEMORY: Linking Sidebar to Main Search ---
if 'daily_cal' not in st.session_state:
    st.session_state.daily_cal = 0
if 'daily_pro' not in st.session_state:
    st.session_state.daily_pro = 0

# --- SIDEBAR: Interconnected 28-Day Challenge ---
with st.sidebar:
    st.header("🏁 28-Day Health Tracker")
    user_goal = st.selectbox("Select Your Goal:", ["Weight Loss", "Weight Gain", "Muscle Building"])
    weight_target = st.number_input("Target Weight (kg)", 1, 20, 5)
    
    # Logic: Goal ke mutabiq limit set karna
    daily_limit = 1600 if user_goal == "Weight Loss" else 2800
    
    st.markdown("---")
    st.subheader("📊 Today's Progress")
    st.metric("Calories Eaten", f"{st.session_state.daily_cal} kcal")
    st.metric("Protein Intake", f"{st.session_state.daily_pro}g")
    
    # Progress Bar (Interconnected)
    remaining = daily_limit - st.session_state.daily_cal
    st.write(f"**Remaining:** {remaining} kcal")
    st.progress(min(st.session_state.daily_cal / daily_limit, 1.0))
    
    if st.button("Reset Today's Stats"):
        st.session_state.daily_cal = 0
        st.session_state.daily_pro = 0
        st.rerun()

# --- MAIN APP ---
st.title("👨‍⚕️ Pro AI Health Engine")
st.write(f"Goal: **{user_goal}** | Challenge Day: **{date.today().day % 28}**")

# Comprehensive Professional Database
meal_db = {
    "paratha": {
        "cal": 290, "pro": 6, "fat": 15, "carb": 42, "min": "Iron, Sodium", "type": "bad",
        "doc": "Medical Warning: High saturated fats. Senior Doctors suggest switching to Multigrain Roti for heart health."
    },
    "egg": {
        "cal": 78, "pro": 7, "fat": 5, "carb": 0.6, "min": "Zinc, Vitamin D, B12", "type": "good",
        "doc": "Clinical Advice: Pure protein source. 2 boiled eggs are highly recommended for muscle recovery."
    },
    "biryani": {
        "cal": 480, "pro": 18, "fat": 22, "carb": 65, "min": "Sodium, Potassium", "type": "bad",
        "doc": "Specialist Note: High sodium retention risk. Avoid eating this at night during your 28-day challenge."
    },
    "roti": {
        "cal": 120, "pro": 4, "fat": 0.5, "carb": 26, "min": "Fiber, Magnesium", "type": "good",
        "doc": "Doctor's Advice: Excellent for weight loss. Keeps your insulin stable and digestion smooth."
    },
    "nihari": {
        "cal": 550, "pro": 25, "fat": 35, "carb": 15, "min": "Iron, Calcium", "type": "bad",
        "doc": "Doctor's Warning: Extreme lipid content in marrow. Avoid if you have high blood pressure."
    },
    "chicken grill": {
        "cal": 230, "pro": 31, "fat": 4, "carb": 0, "min": "B6, Zinc, Phosphorus", "type": "good",
        "doc": "Expert Choice: The gold standard for fat loss and muscle building. Pair with lemon water."
    },
    "apple": {
        "cal": 52, "pro": 0.3, "fat": 0.2, "carb": 14, "min": "Vitamin C, Fiber", "type": "good",
        "doc": "Health Fact: High pectin fiber helps lower cholesterol. Ideal mid-day snack."
    }
}

# Search and Action Area
query = st.text_input("Aapne aaj kya khaya?", placeholder="Type here (egg, paratha, biryani...)").lower()

if query:
    found = False
    for meal, data in meal_db.items():
        if meal in query:
            found = True
            st.markdown(f"""
            <div class="report-container">
                <h2 style="color:#4CAF50;">📋 Analysis Report: {meal.upper()}</h2>
                <div class="data-line">🔥 Calories: <span class="value">{data['cal']} kcal</span></div>
                <div class="data-line">💪 Protein: <span class="value">{data['pro']}g</span></div>
                <div class="data-line">🍔 Total Fats: <span class="value">{data['fat']}g</span></div>
                <div class="data-line">🍞 Carbohydrates: <span class="value">{data['carb']}g</span></div>
                <div class="data-line">🧪 Essential Minerals: <span class="value">{data['min']}</span></div>
            """)

            # --- RED FLAG LOGIC: Goal-Based Warnings ---
            if user_goal == "Weight Loss" and data['type'] == "bad":
                st.markdown('<div class="red-flag">🚩 RED FLAG: Yeh khana aapke Weight Loss goal ke khilaf hai!</div>', unsafe_allow_html=True)
            elif user_goal == "Weight Gain" and meal == "apple":
                st.markdown('<div class="red-flag">🚩 NOTE: Sirf phal kafi nahi, aapko zyada calories ki zaroorat hai!</div>', unsafe_allow_html=True)

            st.markdown(f"""
                <div class="doctor-advice">
                    <span class="medical-tag">👨‍⚕️ Senior Doctor's Advice:</span><br>
                    <p style="margin-top:10px;">{data['doc']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # --- INTERCONNECTION BUTTON ---
            if st.button(f"Add {meal.capitalize()} to Today's Challenge"):
                st.session_state.daily_cal += data['cal']
                st.session_state.daily_pro += data['pro']
                st.success(f"{meal.capitalize()} added! Check your Sidebar.")
                st.rerun()

    if not found:
        st.info("🤖 AI is scanning medical records for this specific dish...")

st.divider()
st.caption("Developed by Abbas Ali | Everything Integrated V10.0")
