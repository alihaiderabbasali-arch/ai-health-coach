import streamlit as st
from datetime import date
import pandas as pd
import re
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Gemini Health Engine", page_icon="👨‍⚕️", layout="centered")

# --- CLEAN DESIGN (No Bugs) ---
st.markdown("""
    <style>
    .report-card { 
        background-color: #1e2130; padding: 20px; border-radius: 15px; 
        border: 2px solid #4CAF50; color: white; margin-bottom: 15px;
    }
    .metric-line { display: flex; justify-content: space-between; border-bottom: 1px solid #333; padding: 8px 0; }
    .m-label { color: #aaa; }
    .m-val { color: #4CAF50; font-weight: bold; }
    .red-flag { background-color: #451313; color: #ff4b4b; padding: 10px; border-radius: 10px; text-align: center; margin-top: 10px; border: 1px solid #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# --- APP LOGIC & MEMORY ---
if 'daily_cal' not in st.session_state: st.session_state.daily_cal = 0
if 'daily_pro' not in st.session_state: st.session_state.daily_pro = 0

# --- SIDEBAR ---
with st.sidebar:
    st.header("🏁 28-Day Tracker")
    u_goal = st.selectbox("Select Goal:", ["Weight Loss", "Weight Gain", "Muscle Building"])
    limit = 1600 if u_goal == "Weight Loss" else 2800
    
    st.metric("Total Calories", f"{st.session_state.daily_cal} kcal")
    st.metric("Total Protein", f"{st.session_state.daily_pro} g")
    st.progress(min(st.session_state.daily_cal / limit, 1.0))
    
    if st.button("Reset Stats"):
        st.session_state.daily_cal, st.session_state.daily_pro = 0, 0
        st.rerun()

# --- MAIN INTERFACE ---
st.title("👨‍⚕️ Gemini Pro Health AI")
st.write(f"**Goal:** {u_goal} | **Challenge Day:** {date.today().day % 28}")

# Master Dictionary
food_db = {
    "chai": {"tags": ["chai", "tea", "doodh patti"], "cal": 90, "pro": 2, "type": "neutral", "doc": "Limit sugar. Keep gap from meals."},
    "paratha": {"tags": ["paratha", "pratha", "porota"], "cal": 290, "pro": 6, "type": "bad", "doc": "High saturated fats. Avoid in weight loss."},
    "egg": {"tags": ["egg", "anda", "boiled egg"], "cal": 78, "pro": 7, "type": "good", "doc": "Pure protein. Best for muscle recovery."},
    "biryani": {"tags": ["biryani", "rice", "chawal"], "cal": 480, "pro": 18, "type": "bad", "doc": "High carb/sodium. Portion control needed."}
}

query = st.text_input("Aap ne aaj kya khaya?", placeholder="e.g. Maine 2 anday aur 1 chai pi...").lower()

if query:
    matched = False
    for item, data in food_db.items():
        if any(tag in query for tag in data["tags"]):
            matched = True
            
            # Simple Quantity Extraction
            qty_match = re.search(r'(\d+)', query)
            qty = int(qty_match.group(1)) if qty_match else 1
            
            # 1. Analysis Report
            st.markdown(f"""
            <div class="report-card">
                <h2 style="color:#4CAF50; text-align:center;">📋 {item.upper()} REPORT</h2>
                <div class="metric-line"><span class="m-label">🔥 Calories</span><span class="m-val">{data['cal'] * qty} kcal</span></div>
                <div class="metric-line"><span class="m-label">💪 Protein</span><span class="m-val">{data['pro'] * qty} g</span></div>
            </div>
            """, unsafe_allow_html=True)

            # 2. Red Flag
            if u_goal == "Weight Loss" and data['type'] == "bad":
                st.markdown(f'<div class="red-flag">🚩 RED FLAG: {item.capitalize()} goal ke khilaf hai!</div>', unsafe_allow_html=True)

            # 3. Clean Doctor Advice
            st.info(f"👨‍⚕️ **DOCTOR'S ADVICE:** {data['doc']}")
            
            # 4. Action Button
            if st.button(f"Add {item.capitalize()} to Progress"):
                st.session_state.daily_cal += (data['cal'] * qty)
                st.session_state.daily_pro += (data['pro'] * qty)
                st.rerun()
            break

    if not matched:
        st.warning("🤖 AI is scanning... Dish milti-julti nahi hai.")

st.divider()
st.caption("Developed by Abbas Ali | Gemini Integrated V17.0 Stable")
