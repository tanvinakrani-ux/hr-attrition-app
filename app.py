import streamlit as st

# Set up page title and icon
st.set_page_config(page_title="HR Employee Attrition Portal", page_icon="👥")

# Page Title
st.title("👥 HR Employee Attrition & Flight-Risk Portal")
st.write("An interactive analytics tool for evaluating employee retention risk.")

st.markdown("---")

# Sidebar for HR Inputs
st.sidebar.header("Employee Details")

dept = st.sidebar.selectbox("Department", ["Sales", "Research & Development", "Human Resources"])
satisfaction = st.sidebar.slider("Job Satisfaction (1 = Low, 4 = High)", 1, 4, 3)
balance = st.sidebar.slider("Work-Life Balance (1 = Poor, 4 = Best)", 1, 4, 2)
tenure = st.sidebar.number_input("Years at Company", min_value=0, max_value=40, value=3)
overtime = st.sidebar.radio("Works Overtime?", ["Yes", "No"])

# Attrition Risk Calculation Engine
risk_score = 0

if satisfaction <= 2:
    risk_score += 35
if balance <= 2:
    risk_score += 25
if overtime == "Yes":
    risk_score += 30
if tenure < 2:
    risk_score += 10

# Results Display
st.subheader(f"Assessment Results: {dept} Department")
st.metric(label="Calculated Attrition Risk", value=f"{risk_score}%")

if risk_score >= 60:
    st.error("⚠️ HIGH ATTRITION RISK: Immediate HR intervention required.")
    st.write("• Schedule a 1-on-1 stay interview.")
    st.write("• Review workload and overtime expectations.")
elif risk_score >= 35:
    st.warning("⚡ MODERATE ATTRITION RISK: Monitor engagement closely.")
    st.write("• Discuss career growth and compensation goals.")
else:
    st.success("✅ LOW ATTRITION RISK: High retention stability.")