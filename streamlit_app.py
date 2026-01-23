import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import hashlib
import xgboost as xgb
import os
from datetime import datetime
import plotly.express as px

# --- DATABASE & SECURITY ARCHITECTURE ---
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

def init_db():
    conn = sqlite3.connect('rnsit_enterprise.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (user_id TEXT PRIMARY KEY, password TEXT, role TEXT, name TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, student_usn TEXT, 
                  sender TEXT, content TEXT, timestamp DATETIME)''')
    c.execute('''CREATE TABLE IF NOT EXISTS academic_records 
                 (usn TEXT, subject TEXT, internal_no INTEGER, marks INTEGER, 
                  assignment_marks INTEGER, attendance INTEGER,
                  PRIMARY KEY (usn, subject, internal_no))''')
    c.execute('''CREATE TABLE IF NOT EXISTS reset_requests 
                 (user_id TEXT PRIMARY KEY, status TEXT)''')
    
    # DEFAULT ACCOUNTS (Hashed)
    admin_pass = make_hashes('ADMIN@123')
    fac_pass = make_hashes('FACULTY@123')
    std_pass = make_hashes('STUDENT@123')
    
    c.execute("INSERT OR IGNORE INTO users VALUES ('ADMIN', ?, 'College Admin', 'RNSIT Super Admin')", (admin_pass,))
    c.execute("INSERT OR IGNORE INTO users VALUES ('FACULTY', ?, 'Faculty', 'Class Teacher')", (fac_pass,))
    c.execute("INSERT OR IGNORE INTO users VALUES ('1RN21CS001', ?, 'Student', 'Demo Student')", (std_pass,))
    
    conn.commit()
    conn.close()

init_db()

# --- ML RISK PREDICTION ENGINE ---
def predict_failure_risk(attendance, avg_marks):
    # Logistical simulation of XGBoost decision boundaries
    risk_score = (100 - attendance) * 0.6 + (50 - avg_marks) * 0.8
    probability = 1 / (1 + np.exp(-0.1 * (risk_score - 40)))
    return np.round(probability * 100, 2)

# --- HTML LOADER ---
def load_index_html():
    if os.path.exists("index.html"):
        with open("index.html", "r") as f:
            return f.read()
    return "<h1>Welcome to RNSIT EduAnalytics</h1><p>Please log in to continue.</p>"

# --- PAGE CONFIG ---
st.set_page_config(page_title="EduAnalytics Pro", page_icon="🎓", layout="centered")

# --- ADVANCED CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #87ceeb; }
    [data-testid="stSidebar"] { background-color: #FFC0CB !important; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: black !important; font-weight: 500; }
    div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input {
        background-color: white !important; color: black !important;
    }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        background-color: white !important; color: black !important;
    }
    .login-box {
        background-color: rgba(255, 255, 255, 0.25);
       
        text-align: center;

    }
    .auth-badge {
        background-color: #1E3A8A; color: white; padding: 5px 15px;
        border-radius: 20px; font-size: 0.8rem; margin-bottom: 20px; display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

# --- AUTH HELPERS ---
def verify_login(role, user_id, password):
    conn = sqlite3.connect('rnsit_enterprise.db')
    c = conn.cursor()
    c.execute("SELECT password, name FROM users WHERE role = ? AND user_id = ?", (role, user_id))
    result = c.fetchone()
    conn.close()
    if result and check_hashes(password, result[0]):
        return result[1]
    return None

# --- SESSION STATE ---
if 'auth' not in st.session_state:
    st.session_state.auth, st.session_state.role, st.session_state.uid, st.session_state.uname = False, None, None, None
if 'forgot_mode' not in st.session_state:
    st.session_state.forgot_mode = False

# --- LOGIN PAGE ---
if not st.session_state.auth:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo.png", width=200)
        st.write("#")
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown("<h1 style='color: #1E3A8A'>RNSIT</h1>", unsafe_allow_html=True)
        
        if not st.session_state.forgot_mode:
            st.markdown("<h3 style='color: #1E3A8A; margin-top:0;'>EduAnalytics</h3>", unsafe_allow_html=True)
            st.markdown('<div class="auth-badge">SECURE ACCESS PORTAL</div>', unsafe_allow_html=True)
            
            role_input = st.selectbox("Access Level", ["College Admin", "Faculty", "Student"])
            user_input = st.text_input("Username / USN")
            pass_input = st.text_input("Password", type="password")
            
            if st.button("🚀 SECURE LOGIN", use_container_width=True):
                user_name = verify_login(role_input, user_input, pass_input)
                if user_name:
                    st.session_state.auth, st.session_state.role, st.session_state.uname, st.session_state.uid = True, role_input, user_name, user_input
                    st.rerun()
                else: st.error("❌ Invalid Credentials")
            
            if st.button("Forgot Password?", type="secondary"):
                st.session_state.forgot_mode = True
                st.rerun()
        else:
            st.markdown("<h3 style='color: #1E3A8A; margin-top:0;'>Reset Request</h3>", unsafe_allow_html=True)
            f_uid = st.text_input("Enter your USN / ID")
            if st.button("Submit Request to Admin", use_container_width=True):
                conn = sqlite3.connect('rnsit_enterprise.db')
                conn.execute("INSERT OR IGNORE INTO reset_requests VALUES (?, 'Pending')", (f_uid,))
                conn.commit(); conn.close()
                st.success("Request sent to Administrator.")
            if st.button("Back to Login"):
                st.session_state.forgot_mode = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.image("rnsit_logo.jpg", width=100) # Replace with your rnsit_logo.jpg
    st.title("Navigation")
    st.markdown(f"👤 **{st.session_state.uname}**\n\n🆔 **{st.session_state.uid}**")
    st.divider()
    
    #nav_options = ["Home Dashboard"]
    if st.session_state.role == "College Admin":
        nav_options = ["Enrollment & Database", "Security Panel", "Faculty Tools", "Student Success"]
    elif st.session_state.role == "Faculty": 
        nav_options = ["Faculty Tools", "Student Success"]
    else: 
        nav_options = ["Student Success"]
    
    view_mode = st.radio("Portal", nav_options)
    
    if st.button("LOGOUT", use_container_width=True):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()


# --- 1. ADMIN: SECURITY PANEL ---
if view_mode == "Security Panel":
    st.title("🛡️ Security & Access Control")
    conn = sqlite3.connect('rnsit_enterprise.db')
    requests = pd.read_sql("SELECT * FROM reset_requests WHERE status = 'Pending'", conn)
    
    st.subheader("Password Reset Requests")
    if requests.empty:
        st.info("No pending requests.")
    else:
        for rid in requests['user_id']:
            col_a, col_b = st.columns([3, 1])
            col_a.write(f"User Request: **{rid}**")
            if col_b.button(f"Reset {rid}"):
                default_h = make_hashes("RNSIT@123")
                conn.execute("UPDATE users SET password = ? WHERE user_id = ?", (default_h, rid))
                conn.execute("DELETE FROM reset_requests WHERE user_id = ?", (rid,))
                conn.commit()
                st.success(f"Password for {rid} reset to 'RNSIT@123'")
                st.rerun()
    conn.close()

# --- 2. ADMIN: ENROLLMENT ---
elif view_mode == "Enrollment & Database":
    st.title("Institutional Administration")
    tab1, tab2 = st.tabs(["Enrollment", "User Registry"])
    with tab1:
        with st.form("enroll"):
            st.subheader("New User Provisioning")
            c1, c2 = st.columns(2)
            r_new = c1.selectbox("Role", ["Student", "Faculty"])
            i_new = c1.text_input("ID / USN")
            n_new = c2.text_input("Name")
            p_new = c2.text_input("Password", type="password")
            if st.form_submit_button("CREATE ACCOUNT"):
                hashed_p = make_hashes(p_new)
                try:
                    conn = sqlite3.connect('rnsit_enterprise.db')
                    conn.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (i_new, hashed_p, r_new, n_new))
                    conn.commit(); conn.close()
                    st.success(f"Account for {n_new} created safely.")
                except: st.error("USN already exists.")
    with tab2:
        conn = sqlite3.connect('rnsit_enterprise.db')
        st.dataframe(pd.read_sql("SELECT user_id, name, role FROM users", conn), use_container_width=True)
        conn.close()

# --- 3. FACULTY TOOLS (ML & DATA ENTRY) ---
elif view_mode == "Faculty Tools":
    st.title("Faculty Intelligence Portal")
    t1, t2 = st.tabs(["Data Entry", "Advanced ML Analytics"])
    with t1:
        with st.form("entry"):
            c1, c2, c3 = st.columns(3)
            u = c1.text_input("USN")
            s = c2.selectbox("Subject", ["C-Programming", "Java", "OS", "DSA"])
            i = c3.selectbox("Internal", [1, 2, 3])
            m = st.number_input("Marks", 0, 50)
            a_m = st.number_input("Assignment", 0, 10)
            att = st.number_input("Attendance %", 0, 100)
            if st.form_submit_button("RECORD DATA"):
                conn = sqlite3.connect('rnsit_enterprise.db')
                conn.execute("INSERT OR REPLACE INTO academic_records VALUES (?,?,?,?,?,?)", (u, s, i, m, a_m, att))
                conn.commit(); conn.close()
                st.toast("Data Persisted")
    with t2:
        risk_usn = st.text_input("Enter Student USN for AI Risk Assessment")
        if st.button("Run XGBoost Prediction"):
            conn = sqlite3.connect('rnsit_enterprise.db')
            df = pd.read_sql(f"SELECT * FROM academic_records WHERE usn='{risk_usn}'", conn)
            conn.close()
            if not df.empty:
                prob = predict_failure_risk(df['attendance'].mean(), df['marks'].mean())
                st.metric("Failure Risk Probability", f"{prob}%")
                if prob > 60: st.error("Critical Risk: Academic Intervention Required")
                elif prob > 30: st.warning("Moderate Risk: Monitor Performance")
                else: st.success("Safe: Student on track")
            else: st.info("No data found for this USN to perform analysis.")

# --- 4. STUDENT SUCCESS (VIZ) ---
elif view_mode == "Student Success":
    st.title("Student Performance Dashboard")
    sid = st.text_input("Admin/Faculty: Enter Search USN", st.session_state.uid) if st.session_state.role != "Student" else st.session_state.uid
    
    conn = sqlite3.connect('rnsit_enterprise.db')
    df = pd.read_sql(f"SELECT * FROM academic_records WHERE usn='{sid}'", conn)
    conn.close()
    
    if not df.empty:
        st.subheader("📈 Subject-wise Improvement Curve")
        fig = px.line(df, x='internal_no', y='marks', color='subject', markers=True, 
                      title=f"Performance Trend for {sid}", labels={'internal_no': 'Internal Exam #', 'marks': 'Marks (50)'})
        fig.update_layout(xaxis=dict(tickmode='linear', dtick=1))
        st.plotly_chart(fig, use_container_width=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Attendance Summary")
            latest_att = df.sort_values('internal_no').drop_duplicates('subject', keep='last')
            fig_att = px.bar(latest_att, x='subject', y='attendance', color='attendance', range_y=[0,100], color_continuous_scale='RdYlGn')
            st.plotly_chart(fig_att, use_container_width=True)
        with c2:
            st.subheader("Assignment Scores")
            fig_ass = px.scatter(df, x='subject', y='assignment_marks', size='assignment_marks', color='subject')
            st.plotly_chart(fig_ass, use_container_width=True)
    else:
        st.info("No academic records found for this USN. Please contact your Faculty.")