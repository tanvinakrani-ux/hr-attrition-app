import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

st.set_page_config(page_title="HR Attrition & Analytics Portal", layout="wide")

st.title("📊 HR Employee Attrition & Analytics Portal")

# Main Navigation Tabs
tab1, tab2, tab3 = st.tabs([
    "🧮 Individual Risk Assessment", 
    "📁 Batch CSV Upload & Analytics", 
    "📈 Tableau Executive Dashboard"
])

# ==================== TAB 1: INDIVIDUAL CALCULATOR ====================
with tab1:
    st.header("Single Employee Flight-Risk Evaluation")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Employee Details")
        dept = st.selectbox("Department", ["Sales", "Research & Development", "Human Resources"])
        satisfaction = st.slider("Job Satisfaction (1-4)", 1, 4, 3)
        balance = st.slider("Work-Life Balance (1-4)", 1, 4, 3)
        tenure = st.number_input("Years at Company", min_value=0, max_value=40, value=2)
        overtime = st.radio("Works Overtime?", ["No", "Yes"])
        
    with col2:
        st.subheader("Risk Score & Recommendation")
        
        # Risk Logic
        risk_score = 0
        if satisfaction <= 2:
            risk_score += 35
        if balance <= 2:
            risk_score += 25
        if overtime == "Yes":
            risk_score += 30
        if tenure < 2:
            risk_score += 10
            
        st.metric(label="Flight Risk Percentage", value=f"{risk_score}%")
        
        if risk_score >= 60:
            st.error("🚨 **High Attrition Risk!** Immediate 1-on-1 Stay Interview recommended.")
        elif risk_score >= 35:
            st.warning("⚠️ **Moderate Attrition Risk.** Monitor engagement and workload closely.")
        else:
            st.success("✅ **Low Attrition Risk.** High employee retention stability.")

# ==================== TAB 2: BATCH CSV & PLOTLY Visuals ====================
with tab2:
    st.header("Batch Assessment & Visual Insights")
    st.write("Upload a CSV file containing employee data to process multiple records simultaneously.")
    
    uploaded_file = st.file_uploader("Upload Employee Data (CSV)", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        # Calculate risk scores across dataframe
        def calculate_risk(row):
            score = 0
            if row.get('JobSatisfaction', 3) <= 2:
                score += 35
            if row.get('WorkLifeBalance', 3) <= 2:
                score += 25
            if str(row.get('OverTime', 'No')).lower() in ['yes', '1', 'true']:
                score += 30
            if row.get('YearsAtCompany', 5) < 2:
                score += 10
            return score

        df['Risk_Score (%)'] = df.apply(calculate_risk, axis=1)
        df['Risk_Level'] = df['Risk_Score (%)'].apply(
            lambda x: 'High' if x >= 60 else ('Moderate' if x >= 35 else 'Low')
        )
        
        st.subheader("Processed Records")
        st.dataframe(df.head(10))
        
        # Feature 1: Download Report Button
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Full Risk Analysis Report (CSV)",
            data=csv_data,
            file_name="HR_Attrition_Risk_Report.csv",
            mime="text/csv"
        )
        
        # Feature 2: Interactive Plotly Visualizations
        st.markdown("---")
        st.subheader("Interactive Visual Analytics")
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            fig_pie = px.pie(df, names='Risk_Level', title="Overall Risk Category Distribution",
                             color='Risk_Level',
                             color_discrete_map={'Low': '#2ecc71', 'Moderate': '#f1c40f', 'High': '#e74c3c'})
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col_chart2:
            if 'Department' in df.columns:
                fig_bar = px.histogram(df, x='Department', color='Risk_Level', barmode='group',
                                       title="Attrition Risk Breakdown by Department")
                st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("💡 **Sample Data Format Required:** CSV with columns: `JobSatisfaction`, `WorkLifeBalance`, `OverTime`, `YearsAtCompany`, `Department`.")

# ==================== TAB 3: MANDATORY TABLEAU DASHBOARD ====================
with tab3:
    st.header("Executive Tableau Analytics Dashboard")
    st.write("Embedded interactive Tableau Public visualization satisfying executive analytics requirements.")
    
    tableau_url = "https://public.tableau.com/views/HR_Attrition_16886470870900/HRAnalytics?:showVizHome=no&:embed=true"
    
    tableau_embed_code = f"""
        <iframe src="{tableau_url}" width="100%" height="700" frameborder="0"></iframe>
    """
    
    components.html(tableau_embed_code, height=720, scrolling=True)