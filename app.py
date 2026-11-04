import streamlit as st
import pandas as pd
import plotly.express as px
from google import genai

# Page Setup
st.set_page_config(page_title="Advanced AI Patient Health Analyzer", page_icon="🏥", layout="wide")

# Initialize Gemini Client using Streamlit Secrets
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    client = None

st.title("🏥 Advanced AI-Based Patient Health Analyzer")
st.caption("Hospital Clinical Support System Powered by Google Gemini AI")

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
medical_history = st.sidebar.text_area("Existing Medical History", "None reported")

# Core Rule-Based Risk Function
def analyze_health_risk(sys, dia, gluc, bmi_val, symp_list):
    risks = []
    score = 0
    if sys >= 140 or dia >= 90:
        risks.append("High Blood Pressure (Hypertension)")
        score += 2
    elif sys >= 120 or dia >= 80:
        risks.append("Pre-hypertension Alert")
        score += 1
    if gluc >= 126:
        risks.append("High Fasting Glucose (Potential Diabetes)")
        score += 2
    elif gluc >= 100:
        risks.append("Impaired Fasting Glucose (Pre-diabetes)")
        score += 1
    if bmi_val >= 30:
        risks.append("Obesity (Elevated Cardiovascular Risk)")
        score += 2
    elif bmi_val >= 25:
        risks.append("Overweight Status")
        score += 1
    if "Chest Pain" in symp_list or "Shortness of Breath" in symp_list:
        risks.append("Acute Cardiac Symptom Indicator")
        score += 3
        
    if score >= 5:
        category = "High Risk"
    elif score >= 2:
        category = "Moderate Risk"
    else:
        category = "Low Risk"
    return category, risks

risk_cat, risk_factors = analyze_health_risk(sys_bp, dia_bp, glucose, bmi, symptoms)

# Tabs Navigation
tab1, tab2, tab3, tab4 = st.tabs(["📊 Diagnostic Dashboard", "🤖 Gemini AI Clinical Report", "💊 Treatment Plan", "⚖️ AI Ethics"])

with tab1:
    col1, col2, col3 = st.columns(3)
    col1.metric("Patient Name", patient_name)
    col2.metric("Overall Risk Status", risk_cat)
    col3.metric("Blood Pressure", f"{sys_bp}/{dia_bp} mmHg")
    
    st.divider()
    st.subheader("⚠️ Identified Health Risk Factors")
    if risk_factors:
        for rf in risk_factors:
            st.error(f"• {rf}")
    else:
        st.success("No critical high-risk indicators detected.")

    vitals_df = pd.DataFrame({
        'Metric': ['Systolic BP', 'Diastolic BP', 'Fasting Glucose', 'BMI x 4'],
        'Value': [sys_bp, dia_bp, glucose, bmi * 4]
    })
    fig = px.bar(vitals_df, x='Metric', y='Value', title="Patient Vitals Overview", color='Metric')
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("🧠 Gemini AI Advanced Diagnostic Summary")
    st.markdown("Click the button below to generate a real-time clinical analysis and risk assessment using Gemini AI.")
    
    if st.button("Generate AI Medical Summary 🚀"):
        if client is None:
            st.error("Gemini API key not configured properly in secrets.toml!")
        else:
            with st.spinner("Gemini is analyzing patient records and clinical parameters..."):
                prompt = f"""
                You are an expert clinical assistant. Analyze the following patient data and provide a professional medical summary, potential differential insights, and recommendations for the attending physician.
                
                Patient Details:
                - Name: {patient_name}
                - Age: {age}, Gender: {gender}
                - Systolic BP: {sys_bp} mmHg
                - Diastolic BP: {dia_bp} mmHg
                - Fasting Glucose: {glucose} mg/dL
                - BMI: {bmi}
                - Symptoms: {', '.join(symptoms) if symptoms else 'None'}
                - Medical History: {medical_history}
                - Computed Risk Category: {risk_cat}
                
                Format the output clearly with markdown headings: Clinical Impressions, Risk Assessment, and Recommended Diagnostic Next Steps.
                """
                
                try:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt
                    )
                    st.success("Analysis Complete!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error generating AI response: {e}")

with tab3:
    st.subheader("💡 Recommended Care Plan")
    if risk_cat == "High Risk":
        st.warning("🚨 **Immediate Doctor Consultation Recommended**")
        st.markdown("- Order comprehensive blood work (HbA1c, Lipid Profile).")
        st.markdown("- Initiate cardiology or endocrinology specialist referral.")
    elif risk_cat == "Moderate Risk":
        st.info("🟡 **Lifestyle & Dietary Intervention**")
        st.markdown("- Introduce low-sodium diet and daily aerobic monitoring.")
        st.markdown("- Re-check vitals after 30 days.")
    else:
        st.success("🟢 **Maintenance & Wellness**")
        st.markdown("- Encourage routine annual preventative screenings.")

with tab4:
    st.subheader("⚖️ AI Medical Solution Evaluation & Governance")
    st.markdown("- **Clinical Oversight:** All AI-generated recommendations require human physician validation.")
    st.markdown("- **Data Privacy:** Compliant with simulated secure healthcare record handling.")

st.sidebar.divider()
st.sidebar.caption("🔒 Advanced Medical Decision Support Demo")