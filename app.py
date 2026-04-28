import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="Smart Community | Prime Circle", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { background-color: #4285F4; color: white; border-radius: 5px; }
    .priority-high { color: red; font-weight: bold; }
    </style>
    """, unsafe_allow_index=True)

# --- MOCK DATA STORAGE (In a real app, this would be SQLite/Cloud SQL) ---
if 'needs' not in st.session_state:
    st.session_state.needs = [
        {"id": 1, "issue": "Pipe Leakage", "category": "Water", "location": "Sector 12", "severity": 5, "frequency": 4, "status": "Pending"},
        {"id": 2, "issue": "Street Light Broken", "category": "Infrastructure", "location": "Green Park", "severity": 2, "frequency": 3, "status": "In Progress"}
    ]

if 'volunteers' not in st.session_state:
    st.session_state.volunteers = [
        {"name": "Rahul Sharma", "skill": "Plumbing", "location": "Sector 12", "available": True},
        {"name": "Aditi Tathe", "skill": "Education", "location": "Green Park", "available": True},
        {"name": "Amit Verma", "skill": "Electrician", "location": "Sector 5", "available": True}
    ]

# --- SIDEBAR NAVIGATION ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/924/924514.png", width=100)
st.sidebar.title("Prime Circle")
menu = st.sidebar.radio("Navigation", ["Dashboard", "Report a Need", "Volunteer Directory", "Smart Matching"])

# --- DASHBOARD ---
if menu == "Dashboard":
    st.title("📊 NGO Admin Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Active Needs", len(st.session_state.needs))
    col2.metric("Total Volunteers", len(st.session_state.volunteers))
    col3.metric("Tasks Completed", "76")
    col4.metric("Avg. Response Time", "3.4 Hrs")

    st.subheader("Recent Community Needs")
    df_needs = pd.DataFrame(st.session_state.needs)
    # Calculate Priority Score (Simplified)
    df_needs['Priority Score'] = (df_needs['severity'] + df_needs['frequency']) / 2
    st.table(df_needs[['issue', 'category', 'location', 'Priority Score', 'status']])

# --- DATA COLLECTION (REPORT A NEED) ---
elif menu == "Report a Need":
    st.title("📝 Report Community Need")
    with st.form("need_form"):
        issue = st.text_input("What is the problem? (e.g. Broken Well)")
        cat = st.selectbox("Category", ["Water", "Health", "Education", "Infrastructure", "Environment"])
        loc = st.text_input("Location/Neighborhood")
        sev = st.slider("Severity (1 = Low, 5 = Urgent)", 1, 5)
        freq = st.slider("Frequency (How many people affected?)", 1, 5)
        submitted = st.form_submit_button("Submit to Database")
        
        if submitted:
            new_need = {"id": len(st.session_state.needs)+1, "issue": issue, "category": cat, "location": loc, "severity": sev, "frequency": freq, "status": "Pending"}
            st.session_state.needs.append(new_need)
            st.success("Need registered and prioritized by AI!")

# --- VOLUNTEER DIRECTORY ---
elif menu == "Volunteer Directory":
    st.title("🤝 Volunteer Database")
    df_vol = pd.DataFrame(st.session_state.volunteers)
    st.dataframe(df_vol, use_container_width=True)

# --- SMART MATCHING ENGINE ---
elif menu == "Smart Matching":
    st.title("🤖 AI-Driven Volunteer Matching")
    
    selected_need = st.selectbox("Select a Need to Resolve", [n['issue'] for n in st.session_state.needs if n['status'] == "Pending"])
    
    if selected_need:
        # Simple Logic: Match by Category/Skill and Location
        need_details = next(item for item in st.session_state.needs if item['issue'] == selected_need)
        st.info(f"Targeting: {selected_need} in {need_details['location']}")
        
        st.subheader("Best Matched Volunteers")
        matches = []
        for v in st.session_state.volunteers:
            score = 0
            if v['location'] == need_details['location']: score += 50
            # Logic for skill match (simplified)
            if (need_details['category'] == "Water" and v['skill'] == "Plumbing"): score += 50
            if (need_details['category'] == "Infrastructure" and v['skill'] == "Electrician"): score += 50
            
            matches.append({"Name": v['name'], "Skill": v['skill'], "Match Score": f"{score}%"})
        
        st.table(pd.DataFrame(matches).sort_values(by="Match Score", ascending=False))
        
        if st.button("Assign Task"):
            st.success(f"Task assigned to {matches[0]['Name']}! SMS Notification sent.")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.write("Built for Google Solution Challenge 2024")