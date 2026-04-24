import streamlit as st
from datetime import date

# 1. Page Configuration
st.set_page_config(page_title="AI Health Coach PRO", page_icon="👨‍⚕️", layout="centered")

# 2. Advanced CSS (Everything Combined & Fixed)
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
        background-color: rgba(255, 0, 0, 0.2); padding: 1
