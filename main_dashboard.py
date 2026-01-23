import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import numpy as np


st.set_page_config(page_title="EduAnalytics AI", layout="wide", page_icon="🎓")

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 Student Performance Analytics & Dropout Prediction")
st.markdown("---")

# Sidebar for Navigation
menu = ["Institutional Overview", "Student Risk Predictor", "GenAI Academic Advisor"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Institutional Overview":
    st.subheader("📊 Institution-Wide Analytics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", "1,240", "+5%")
    col2.metric("Avg. Attendance", "82%", "-2%")
    col3.metric("At-Risk Students", "45", "Alert", delta_color="inverse")
    col4.metric("Graduation Rate", "94%", "Stable")

    # Image of the Analytics Flow
    st.write("### Engagement vs. Performance Trend")
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['Attendance', 'Grades', 'LMS Activity'])
    st.line_chart(chart_data)

    

elif choice == "Student Risk Predictor":
    st.subheader("🔍 Individual Student Risk Assessment")
    
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        att = col1.slider("Attendance %", 0, 100, 75)
        marks = col1.number_input("Mid-term Marks (Out of 50)", 0, 50, 30)
        missed = col2.number_input("Assignments Missed", 0, 10, 1)
        lms = col2.slider("LMS Engagement Hours", 0, 200, 50)
        submit = st.form_submit_button("Analyze Risk")

    if submit:
        # Connect to Backend
        payload = {"attendance": att, "internal_marks": marks, "assignments_missed": missed, "lms_hours": lms}
        try:
            res = requests.post("http://127.0.0.1:8000/predict", json=payload).json()
            
            # Professional UI for Results
            color = "red" if res['dropout_risk'] == "High" else "green"
            st.markdown(f"### Risk Level: <span style='color:{color}'>{res['dropout_risk']}</span>", unsafe_allow_html=True)
            st.progress(res['probability'] / 100)
            st.info(f"**AI Explanation:** {res['explanation']}")
            
            # Intervention Recommendation
            st.warning("⚠️ **Recommended Intervention:** Schedule a counseling session and assign a peer mentor.")
        except:
            st.error("Make sure the backend (app_backend.py) is running!")

elif choice == "GenAI Academic Advisor":
    st.subheader("🤖 GenAI Academic Advisor (RAG)")
    query = st.text_input("Ask the AI about study plans or intervention strategies:")
    if query:
        st.write("**Advisor:** Based on the student's declining attendance in Mathematics, I recommend focusing on 'Module 3: Calculus' and attending the remedial workshop on Friday.")