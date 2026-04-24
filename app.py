import streamlit as st

# 1. Page Configuration (Pro Look)
st.set_page_config(page_title="AI Health Coach PRO", page_icon="🥗", layout="centered")

# 2. Professional Styling (CSS)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTextInput>div>div>input { background-color: #1e2130; color: white; border-radius: 10px; }
    .meal-card { 
        background: linear-gradient(135deg, #1e2130 0%, #2b2f44 100%); 
        padding: 25px; 
        border-radius: 20px; 
        border-left: 8px solid #4CAF50; 
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        margin-bottom: 25px;
    }
    .stat-box { 
        background-color: rgba(76, 175, 80, 0.1); 
        padding: 15px; 
        border-radius: 12px; 
        border: 1px solid #4CAF50; 
        text-align: center;
    }
    .doctor-tag { color: #ffcc00; font-weight: bold; font-size: 1.1em; }
    </style>
    """, unsafe_allow_html=True)

# 3. App Header
st.title("🚀 AI Health Coach: Pro Edition")
st.markdown("---")

# 4. Smart Brain (Meal Intelligence Database)
# Isko hum mazeed barhayenge, ye asli logic hai
meal_intelligence = {
    "paratha": {"cal": 290, "pro": 6, "fat": 15, "carb": 42, "doc": "High Carbs! Iske saath protein (eggs) lazmi lein taake sugar spike na ho."},
    "egg": {"cal": 78, "pro": 7, "fat": 5, "carb": 0.6, "doc": "Superfood! Muscles banane ke liye behtareen protein source hai."},
    "roti": {"cal": 120, "pro": 4, "fat": 0.5, "carb": 26, "doc": "Good fiber! Weight loss ke liye parathay se behtar choice hai."},
    "biryani": {"cal": 480, "pro": 18, "fat": 22, "carb": 65, "doc": "Caution: Oil zyada hai. Aaj 30 min extra workout karein."},
    "apple": {"cal": 52, "pro": 0.3, "fat": 0.2, "carb": 14, "advice": "Great snack! Vitamins aur fiber ka khazana."},
    "chicken": {"cal": 239, "pro": 27, "fat": 14, "carb": 0, "doc": "Muscle Recovery King! Isay boil ya grill karke khana best hai."}
}

# 5. User Input Section
st.subheader("📝 Daily Meal Entry")
user_input = st.text_input("Aapne kya khaya? (e.g. 2 egg aur 1 paratha)", placeholder="Yahan type karein...").lower()

if user_input:
    st.markdown("### 📊 AI Nutritional Breakdown")
    found_any = False
    
    # AI Search Logic
    for meal, data in meal_intelligence.items():
        if meal in user_input:
            found_any = True
            # Professional Output Card
            st.markdown(f"""
            <div class="meal-card">
                <h2 style="color:#4CAF50; margin-top:0;">✅ {meal.upper()} Detected</h2>
                <div style="display: flex; justify-content: space-between; gap: 10px;">
                    <div class="stat-box">🔥<br><b>{data['cal']}</b><br>Calories</div>
                    <div class="stat-box">💪<br><b>{data['pro']}g</b><br>Protein</div>
                    <div class="stat-box">🍔<br><b>{data['fat']}g</b><br>Fats</div>
                    <div class="stat-box">🍞<br><b>{data['carb']}g</b><br>Carbs</div>
                </div>
                <hr style="border: 0.5px solid #444;">
                <p class="doctor-tag">👨‍⚕️ Pro Doctor Advice:</p>
                <p style="color: #ddd;">{data['doc']}</p>
            </div>
            """, unsafe_allow_html=True)

    if not found_any:
        st.info("🤖 AI is learning this meal... Humne ise update list mein daal diya hai!")

# 6. Sidebar for 28-Day Tracker
with st.sidebar:
    st.header("🏁 28-Day Challenge")
    st.write("Day: **4 of 28**")
    st.progress(14)
    st.success("Target: 5kg Loss")
    st.markdown("---")
    st.write("🔥 Total Calories Today: **368**")
    st.write("💪 Protein Goal: **45g / 120g**")

st.markdown("---")
st.caption("AI Health Coach V3.0 | Developed by Abbas Ali")
