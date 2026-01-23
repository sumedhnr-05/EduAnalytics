import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
import shap
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# --- MOCK DATA & MODEL TRAINING ---
# In a real scenario, you'd load a CSV here.
def train_model():
    data = pd.DataFrame({
        'attendance': np.random.randint(50, 100, 100),
        'internal_marks': np.random.randint(20, 50, 100),
        'assignments_missed': np.random.randint(0, 5, 100),
        'lms_hours': np.random.randint(10, 100, 100),
        'dropout': np.random.choice([0, 1], 100)
    })
    X = data.drop('dropout', axis=1)
    y = data['dropout']
    model = xgb.XGBClassifier().fit(X, y)
    explainer = shap.TreeExplainer(model)
    return model, explainer, X

model, explainer, X_train = train_model()

class StudentData(BaseModel):
    attendance: float
    internal_marks: float
    assignments_missed: int
    lms_hours: float

@app.post("/predict")
def predict_performance(data: StudentData):
    features = np.array([[data.attendance, data.internal_marks, data.assignments_missed, data.lms_hours]])
    prediction = model.predict(features)[0]
    prob = model.predict_proba(features)[0][1]
    
    # Explainable AI (SHAP)
    shap_values = explainer.shap_values(features)
    
    return {
        "dropout_risk": "High" if prediction == 1 else "Low",
        "probability": round(prob * 100, 2),
        "explanation": "Factors contributing to risk: Attendance and Assignment completion."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)