import streamlit as st

# Page setup
st.set_page_config(page_title="AI Health Coach Pro", page_icon="🛡️")

# Dashboard Title
st.title("🛡️ AI Health Coach: Pro Dashboard")
st.success("App Live Ho Chuki Hai! ✅")

# Sidebar Menu
menu = st.sidebar.radio("Navigation", ["Home", "Meal Tracker", "Medical AI", "Doctor Consultation"])

if menu == "Home":
    st.header("⚖️ Weight & Health Status")
    st.info("Aaj ka status: Balanced. Red Flag system active hai.")
    
elif menu == "Meal Tracker":
    st.header("🥗 Daily Meal Input")
    meal = st.text_input("Kya khaya?")
    cal = st.number_input("Calories", 0)
    if st.button("Add Record"):
        st.write(f"{meal} record kar liya gaya hai!")

elif menu == "Medical AI":
    st.header("🧬 AI Report Scanner")
    st.file_uploader("Upload Report (Image/PDF)")
    st.write("AI analysis report scan karne ke baad yahan dikhayega.")

elif menu == "Doctor Consultation":
    st.header("👨‍⚕️ Expert Mashwara")
    st.write("**Doctor Fee:** 500 PKR / 150 INR")
    if st.button("Pay & Start Chat"):
        st.warning("Payment link generate ho raha hai...")
      
