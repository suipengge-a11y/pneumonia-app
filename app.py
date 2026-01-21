import streamlit as st
import numpy as np

# 1. 页面基本配置
st.set_page_config(page_title="Pediatric Pneumonia Risk Calculator", layout="centered")

# 2. 标题和简介
st.title("🏥 儿童重症肺炎死亡风险预测工具")
st.markdown("---")
st.write("本工具基于多因素 Logistic 回归模型构建，旨在辅助临床医生评估患儿死亡风险。")

# 3. 侧边栏：输入患者临床指标
st.sidebar.header("患者临床指标输入")

# 连续变量
alb = st.sidebar.slider("血清白蛋白 (ALB) g/L", 10.0, 60.0, 35.0, help="入科第1天检测值")
dd = st.sidebar.number_input("D-二聚体 (D-D) mg/L", 0.0, 50.0, 1.0)
bmi = st.sidebar.slider("BMI (kg/m²)", 5.0, 35.0, 16.0)

# 分类变量
adr = st.sidebar.radio("是否使用肾上腺素 (Adrenaline)", ["否 (0)", "是 (1)"])
cpr = st.sidebar.radio("是否进行过 CPR", ["否 (0)", "是 (1)"])

# 4. 变量数值转换
adr_val = 1 if "是" in adr else 0
cpr_val = 1 if "是" in cpr else 0

# 5. 回归系数 (请根据你 Table 2 的真实 Beta 值填入)
# 这里使用的是我们之前讨论的示例值，部署前建议对照你的统计结果核对
intercept = 3.24
b_alb = -0.158
b_dd = 0.245
b_bmi = -0.182
b_adr = 1.42
b_cpr = 1.85

# 6. 计算死亡概率 (Logistic 公式)
logit_p = intercept + (b_alb * alb) + (b_dd * dd) + (b_bmi * bmi) + (b_adr * adr_val) + (b_cpr * cpr_val)
prob = 1 / (1 + np.exp(-logit_p))

# 7. 展示评估结果
st.subheader("📊 风险评估结果")

# 使用列展示结果
col1, col2 = st.columns(2)
with col1:
    st.metric(label="预测死亡概率", value=f"{prob:.1%}")

with col2:
    if prob < 0.3:
        st.success("评估结论：低风险 (Low Risk)")
    elif prob < 0.7:
        st.warning("评估结论：中度风险 (Moderate Risk)")
    else:
        st.error("评估结论：高危风险 (High Risk)")

# 风险进度条
st.progress(prob)

# 底部提示
st.info("💡 提示：本预测结果仅供科研参考，最终临床决策应结合患儿实际病情。")
