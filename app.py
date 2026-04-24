import streamlit as st
from datetime import date

# 1. Page Configuration
st.set_page_config(page_title="AI Health Coach PRO", page_icon="🥗", layout="centered")

# 2. Simple & Clean Styling (Har mobile ke liye best)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .report-container { 
        background-color: #1e2130; 
        padding: 20px; 
        border-radius: 15px; 
        border-left: 5px solid #4CAF50; 
        margin-bottom: 20px;
        color: white;
    }
    .data-line { 
        font-size: 1.1em; 
        margin-bottom: 8px; 
        border-bottom: 1px solid #333;
        padding-bottom: 5px;
    }
    .value { color: #4CAF50; font-weight: bold; float: right; }
    .doctor-advice { 
        background-color: rgba(255, 204, 0, 0.1); 
        padding: 15px; 
        border-radius: 10px; 
        border: 1px solid #ffcc00;
        margin-top: 15px;
        color: #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: 28-DAY CHALLENGE SETTINGS ---
with st.sidebar:
    st.header("🏁 Challenge Settings")
    st.write("Apna target yahan set karein:")
    
    # Target Settings
    weight_target = st.number_input("Weight Loss Goal (kg)", 1, 20, 5)
    start_date = st.date_input("Start Date", date.today())
    
    # Progress Calculation
    st.markdown("---")
    current_day = st.slider("Aaj Konsa Din Hai?", 1, 28, 1)
    progress_val = current_day / 28
    
    st.write(f"📊 **Progress: Day {current_day} of 28**")
    st.progress(progress_val)
    st.success(f"Target: **{weight_target}kg** Kam Karna!")
    st.info("Tip: Rozana meal check-in lazmi karein.")

# --- MAIN APP: MEAL TRACKER ---
st.title("🚀 AI Health Coach PRO")
st.write("Aapne aaj kya khaya? AI se report lein:")

# Smart Database (Simple List Style)
meal_intelligence = {
    "paratha": {"cal": 290, "pro": 6, "fat": 15, "carb": 42, "doc": "Paratha mein carbs aur fats zyada hain. Challenge ke liye iske saath 2 boil anday khayein."},
    "egg": {"cal": 78, "pro": 7, "fat": 5, "carb": 0.6, "doc": "Superfood! Protein se bharpoor. Muscles banane aur weight loss mein madad karta hai."},
    "roti": {"cal": 120, "pro": 4, "fat": 0.5, "carb": 26, "doc": "Best for weight loss! Gandum ki roti fiber ka behtareen zariya hai."},
    "biryani": {"cal": 480, "pro": 18, "fat": 22, "carb": 65, "doc": "Caution: Biryani mein calories bohat zyada hain. Aaj walk double karni paregi!"},
    "nihari": {"cal": 550, "pro": 25, "fat": 35, "carb": 15, "doc": "Protein acha hai magar oil zyada hai. Challenge ke dauran kam hi khayein."},
    "chai": {"cal": 90, "pro": 2, "fat": 3, "carb": 12, "doc": "Sugar kam rakhein. Green tea ya baghair cheeni ki chai behtar hai."}
}

user_input = st.text_input("", placeholder="Type here: egg, paratha, biryani...").lower()

if user_input:
    found = False
    for meal, data in meal_intelligence.items():
        if meal in user_input:
            found = True
            st.markdown(f"""
            <div class="report-container">
                <h2 style="color:#4CAF50; margin-bottom:15px;">✅ {meal.upper()} Report</h2>
                <div class="data-line">🔥 Total Calories: <span class="value">{data['cal']} kcal</span></div>
                <div class="data-line">💪 Protein: <span class="value">{data['pro']}g</span></div>
                <div class="data-line">🍔 Total Fats: <span class="value">{data['fat']}g</span></div>
                <div class="data-line">🍞 Carbohydrates: <span class="value">{data['carb']}g</span></div>
                <div class="doctor-advice">
                    <b style="color:#ffcc00;">👨‍⚕️ Doctor's Advice:</b><br>
                    {data['doc']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    if not found:
        st.info("🤖 AI is checking... Hum jald hi is desi dish ka data add kar denge!")

st.divider()
st.caption("Developed by Abbas Ali | Everything set in one place!")
