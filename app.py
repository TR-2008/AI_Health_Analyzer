import streamlit as st
import pandas as pd
import plotly.express as px

# Page Setup
st.set_page_config(page_title="AI Patient Health Analyzer", page_icon="🏥", layout="wide")

st.title("🏥 AI-Based Patient Health Analyzer")
st.caption("Hospital Clinical Support System & Risk Assessment Tool")

# Sidebar - Patient Information
st.sidebar.header("📋 Patient Demographics & Vitals")

patient_name = st.sidebar.text_input("Patient Name", "John Doe")
age = st.sidebar.number_input("Age", min_value=1, max_value=120, value=45)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
sys_bp = st.sidebar.slider("Systolic BP (mmHg)", 80, 200, 130)
dia_bp = st.sidebar.slider("Diastolic BP (mmHg)", 50, 130, 85)
glucose = st.sidebar.number_input("Fasting Glucose (mg/dL)", 50, 400, 110)
bmi = st.sidebar.number_input("BMI (Body Mass Index)", 10.0, 50.0, 26.5)
symptoms = st.sidebar.multiselect(
    "Observed Symptoms",
    ["Chest Pain", "Shortness of Breath", "Fatigue", "Dizziness", "Frequent Urination", "Blurry Vision"]
)

# Core Analysis Logic
def analyze_health_risk(sys, dia, gluc, bmi_val, symp_list):
    risks = []
    score = 0
    
    # Blood Pressure Logic
    if sys >= 140 or dia >= 90:
        risks.append("High Blood Pressure (Hypertension)")
        score += 2
    elif sys >= 120 or dia >= 80:
        risks.append("Pre-hypertension Alert")
        score += 1
        
    # Glucose Logic
    if gluc >= 126:
        risks.append("High Fasting Glucose (Potential Diabetes)")
        score += 2
    elif gluc >= 100:
        risks.append("Impaired Fasting Glucose (Pre-diabetes)")
        score += 1
        
    # BMI Logic
    if bmi_val >= 30:
        risks.append("Obesity (Elevated Cardiovascular Risk)")
        score += 2
    elif bmi_val >= 25:
        risks.append("Overweight Status")
        score += 1
        
    # Symptom Weighting
    if "Chest Pain" in symp_list or "Shortness of Breath" in symp_list:
        risks.append("Acute Cardiac Symptom Indicator")
        score += 3
        
    # Final Category Determination
    if score >= 5:
        category = "High Risk"
        color = "red"
    elif score >= 2:
        category = "Moderate Risk"
        color = "orange"
    else:
        category = "Low Risk"
        color = "green"
        
    return category, color, risks

risk_cat, risk_color, risk_factors = analyze_health_risk(sys_bp, dia_bp, glucose, bmi, symptoms)

# Tabs Navigation
tab1, tab2, tab3 = st.tabs(["📊 Diagnostic Dashboard", "💊 Treatment & Care Plan", "⚖️ AI Evaluation & Ethics"])

with tab1:
    col1, col2, col3 = st.columns(3)
    col1.metric("Patient Name", patient_name)
    col2.metric("Overall Health Status", risk_cat)
    col3.metric("Systolic / Diastolic BP", f"{sys_bp}/{dia_bp} mmHg")
    
    st.divider()
    
    st.subheader("⚠️ Identified Health Risk Factors")
    if risk_factors:
        for rf in risk_factors:
            st.error(f"• {rf}")
    else:
        st.success("No critical high-risk indicators detected from routine vital inputs.")

    # Vitals Chart
    vitals_df = pd.DataFrame({
        'Metric': ['Systolic BP', 'Diastolic BP', 'Fasting Glucose', 'BMI x 4'],
        'Value': [sys_bp, dia_bp, glucose, bmi * 4]
    })
    fig = px.bar(vitals_df, x='Metric', y='Value', title="Patient Vital Parameters Visualization", color='Metric')
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("💡 Recommended Clinical & Treatment Strategies")
    
    if risk_cat == "High Risk":
        st.warning("🚨 **Immediate Clinical Consultation Required:**")
        st.markdown("- Schedule ECG & Comprehensive Metabolic Panel (CMP).")
        st.markdown("- Evaluate for antihypertensive and anti-diabetic medication therapy.")
        st.markdown("- Direct lifestyle modification with specialized clinical dietitian support.")
    elif risk_cat == "Moderate Risk":
        st.info("🟡 **Preventative Care & Monitoring Plan:**")
        st.markdown("- Re-evaluate blood pressure and glucose levels in 4 weeks.")
        st.markdown("- Implement 150 mins/week moderate aerobic exercise regimen.")
        st.markdown("- Reduce dietary sodium (<2,000 mg/day) and refined sugars.")
    else:
        st.success("🟢 **Routine Maintenance Plan:**")
        st.markdown("- Continue annual routine check-ups.")
        st.markdown("- Maintain balanced diet and hydrated daily routine.")

with tab3:
    st.subheader("⚖️ AI Medical Solution Evaluation")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### ✅ Key Benefits")
        st.markdown("- **Rapid Triage:** Quickly filters high-risk patients for urgent doctor attention.")
        st.markdown("- **Error Reduction:** Provides consistent diagnostic baseline checks.")
        st.markdown("- **Efficiency:** Streamlines clinical workflow and diagnostic planning.")
        
    with col_b:
        st.markdown("### ⚠️ Critical Limitations")
        st.markdown("- **Not a Medical Replacement:** AI offers decision support, not final diagnoses.")
        st.markdown("- **Data Bias Risk:** Predictions depend heavily on training dataset accuracy.")
        st.markdown("- **Privacy Concerns:** Patient record processing requires strict HIPAA compliance.")

st.sidebar.divider()
st.sidebar.caption("🔒 Demo App - For Educational & Clinical Decision Support Purposes Only.")