import streamlit as st
import numpy as np

# 1. Page Configuration (修改浏览器标签页标题)
st.set_page_config(page_title="Pneumonia Risk Calculator", layout="centered")

# 2. Title and Introduction (修改页面主标题)
st.title("🏥 Mortality Risk Calculator for Pediatric Severe Pneumonia")
st.markdown("---")
st.write("This tool is based on a multivariable Logistic regression model to assist clinicians in evaluating mortality risk.")

# 3. Sidebar: Input (修改侧边栏输入)
st.sidebar.header("Clinical Parameters")

# Continuous variables
alb = st.sidebar.slider("Serum Albumin (ALB) g/L", 10.0, 60.0, 35.0)
dd = st.sidebar.number_input("D-dimer (mg/L)", 0.0, 50.0, 1.0)
bmi = st.sidebar.slider("BMI (kg/m²)", 5.0, 35.0, 16.0)

# Categorical variables (修改单选框)
adr = st.sidebar.radio("Adrenaline Use", ["No (0)", "Yes (1)"])
cpr = st.sidebar.radio("History of CPR", ["No (0)", "Yes (1)"])

# 4. Value conversion
adr_val = 1 if "Yes" in adr else 0
cpr_val = 1 if "Yes" in cpr else 0

# 5. Regression Coefficients (系数保持不变)
intercept = 3.24
b_alb = -0.158
b_dd = 0.245
b_bmi = -0.182
b_adr = 1.42
b_cpr = 1.85

# 6. Calculation
logit_p = intercept + (b_alb * alb) + (b_dd * dd) + (b_bmi * bmi) + (b_adr * adr_val) + (b_cpr * cpr_val)
prob = 1 / (1 + np.exp(-logit_p))

# 7. Results (修改结果展示)
st.subheader("📊 Assessment Results")

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Predicted Probability", value=f"{prob:.1%}")

with col2:
    if prob < 0.3:
        st.success("Result: Low Risk")
    elif prob < 0.7:
        st.warning("Result: Moderate Risk")
    else:
        st.error("Result: High Risk")

st.progress(prob)

# Footer (修改页脚提示)
st.info("💡 Note: This tool is for research purposes only and clinical decisions should be made by healthcare professionals.")
