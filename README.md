# RNSIT EduAnalytics Pro

An interactive, high-fidelity web dashboard for institutional intelligence and student success forecasting. This full-stack application provides a modern, dual-themed GUI to execute predictive academic modeling, manage batch student ingestion, track faculty mentorship, and audit security events for institutional compliance.

---

### 🌐 Live Deployment
Explore the live, interactive production application directly in your browser:
🚀 **[EduAnalytics Live Portal](https://eduanalytics-zpwl6eidhjrqzkq2hsuhjz.streamlit.app/)**

---

## 🚀 Overview

**RNSIT EduAnalytics Pro** bridges the gap between academic record-keeping and advanced machine learning. Built specifically for modern educational institutions, it empowers College Administrators, Faculty Advisors, and Students with actionable, predictive insights. 

By analyzing indicators like class attendance, internal exam scores, and learning engagement, the platform predicts student failure risk with SHAP explainability and forecasts future career placement readiness tier-wise.

---

## 🌟 Key Features

* **Dual-Theme Glassmorphism Interface**: Switch dynamically between *Enterprise Midnight (Dark)* and *Arctic Platinum (Light)* themes in real-time. Features custom glassmorphic cards, high-contrast typography, and responsive grid layouts.
* **Batch Ingestion Engine**: Upload class sheets (`.csv`) to parse, validate column schemas, and bulk-load hundreds of academic scores instantly using transactional SQLite execution.
* **Explainable AI (XAI) Risk Profiler**: Uses `XGBoost` and `SHAP` values to calculate individual dropout or failure risks, rendering horizontal contribution charts detailing exactly *why* a student is flagged.
* **AI Career Placement Readiness Forecast**: A multi-class `Random Forest` model predicting whether a student is placed in *Tier 1 (Dream Companies)*, *Tier 2 (Service/Core)*, or *Needs Skill Upgrading*, coupled with an interactive slider sandbox for testing simulated placement readiness.
* **Mentorship & Guidance Log Book**: Allows faculty advisors to log specific action items (e.g., *"Assigned remedial Java classes"*) for flagged students, creating a historical record visible on the student dashboard.
* **Immutable Security & Audit Ledger**: Tracks every critical database transaction (logins, password resets, marks entry, and batch uploads) to maintain an absolute audit trail matching NAAC & NBA institutional requirements.

---

## 🏗️ Architecture & Tech Stack

This project is built using a modern decoupled machine learning architecture:

### Frontend (Streamlit)
* **Framework**: Streamlit (Responsive web interface)
* **Styling**: Vanilla CSS Injection (supporting Glassmorphism, HSL-dynamic custom theme controllers)
* **Data Visualization**: Plotly Express, Plotly Graph Objects
* **State Management**: Native Session State

### Backend & Analytical Engine (Python FastAPI)
* **API Framework**: FastAPI & Uvicorn (port 8000 microservice)
* **ML Stack**: XGBoost, Scikit-Learn (Random Forest Classifier), SHAP (TreeExplainer), Pandas, NumPy
* **Database Layer**: SQLite3 (`rnsit_enterprise.db`) with relational integrity

---

## 📂 Project Structure

```text
EduAnalytics/
├── streamlit_app.py         # Streamlit Application (Dual-Theme Dashboard, Portals, Visuals)
├── main.py                  # FastAPI Backend API (Risk Engine, Placement Models, XAI Attributions)
├── rnsit_enterprise.db      # Production database ledger (Users, Records, Audit, Interventions)
├── requirements.txt         # System & Library dependencies
├── logo.png                 # Main portal branding logo
├── rnsit_logo.jpg           # Sidebar institutional branding logo
└── README.md                # Project documentation & reference
```

---

## 🧠 The ML Analytical Models

The platform operates dual analytical engines via the FastAPI backend:

1. **Academic Failure & Dropout Risk Model (XGBoost)**: Trained on student attendance levels, assignments missed, and average internal assessment scores. Combines output probabilities with SHAP explainability.
2. **Explainable AI Attributions (SHAP)**: Extracts Shapley attribution vectors to show the direct mathematical weight each academic indicator has on raising or lowering a student's risk profile.
3. **Career Placement Readiness Classifier (Random Forest)**: Multi-class classification using inputs like CGPA, DSA coding challenge proficiency, internship counts, projects built, and interview scores to forecast potential placement tiers.

---

## 💻 Getting Started

### Prerequisites
* Python 3.10+
* pip (Python Package Manager)

### Installation

1. **Clone & Navigate to the Project Directory**:
   ```bash
   cd EduAnalytics
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the Database**:
   The database registers its default structures, schema, and accounts automatically when launching `streamlit_app.py` for the first time.

---

## 🏃 Running the Application

### ☁️ Cloud Access (No Setup Required)
Simply navigate to the live deployment link:
👉 **[EduAnalytics Deployed Web App](https://eduanalytics-zpwl6eidhjrqzkq2hsuhjz.streamlit.app/)**

### 💻 Local Run
To experience the full-stack intelligence portal locally, boot both services simultaneously:

1. **Boot the FastAPI Analytical Service**:
   ```bash
   uvicorn main:app --port 8000 --reload
   ```

2. **Launch the Streamlit Enterprise Dashboard**:
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Login Details**:
   Use the default accounts created during initialization (both locally and in the cloud deployment):
   * **College Admin**: ID: `ADMIN` | Pin: `ADMIN@123`
   * **Faculty**: ID: `FACULTY` | Pin: `FACULTY@123`
   * **Student**: ID: `1RN21CS001` | Pin: `STUDENT@123`

---

## 📊 Institutional Accreditation & Standards
The system's built-in **Audit Trail Ledger** and **Mentorship log records** align directly with criteria for institutional accreditations (such as **NBA** and **NAAC** cycles), establishing continuous evaluation loops and accountability reports automatically.
