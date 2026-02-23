import streamlit as st
import time
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import pathlib
from streamlit_lottie import st_lottie
import requests
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# =============================
# PAGE CONFIG
# =============================

st.set_page_config(
    page_title="AI Revenue Intelligence Platform",
    layout="wide"
)

# =============================
# TECH STARTUP DARK STYLING
# =============================
st.markdown("""
<style>

/* ===============================
   GLOBAL ANIMATED BACKGROUND
================================= */

[data-testid="stAppViewContainer"] {
    background: linear-gradient(-45deg, #0f172a, #111827, #0e1117, #1f2937);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    color: white;
}

@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ===============================
   GLASS KPI CARDS
================================= */

[data-testid="stMetric"] {
    background: rgba(22, 26, 35, 0.65);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 25px;
    border: 1px solid rgba(255,255,255,0.05);
    transition: all 0.3s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-8px) scale(1.04);
    box-shadow: 0px 10px 30px rgba(0,0,0,0.6);
}

/* ===============================
   GRADIENT SIDEBAR
================================= */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827, #0e1117);
    border-right: 1px solid rgba(255,255,255,0.05);
}

/* Radio highlight */
div[role="radiogroup"] label {
    padding: 8px 12px;
    border-radius: 10px;
}

div[role="radiogroup"] label:hover {
    background-color: rgba(255,255,255,0.05);
}

/* ===============================
   SUBTLE FOOTER
================================= */

.footer {
    text-align: center;
    padding: 30px 0 10px 0;
    font-size: 13px;
    color: #9ca3af;
}

</style>
""", unsafe_allow_html=True)

# =============================
# GLASS SECTION HELPER
# =============================

def glass_section(title):
    st.markdown(f"""
    <div style="
        background: rgba(22,26,35,0.6);
        backdrop-filter: blur(8px);
        border-radius: 18px;
        padding: 30px;
        margin-bottom: 30px;
        border: 1px solid rgba(255,255,255,0.05);
    ">
    <h2 style='color:white;'>{title}</h2>
    """, unsafe_allow_html=True)


# =============================
# HEADER
# =============================

st.markdown(
    "Real-Time SaaS Performance Monitoring | Forecasting | AI-Powered Churn Detection"
)
st.caption("20,000 Customer Simulation | XGBoost Model | Revenue Risk Engine")

# =============================
# SIDEBAR NAVIGATION
# =============================

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Home",
        "Executive Overview",
        "Revenue Analytics",
        "Forecasting",
        "Risk Intelligence",
        "Customer Insights"
    ]
)


# =============================
# PATH SETUP
# =============================

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

# =============================
# LOAD DATA
# =============================

monthly_revenue = pd.read_csv(BASE_DIR / "data" / "raw" / "monthly_revenue.csv")
customer_month = pd.read_csv(BASE_DIR / "data" / "raw" / "customer_month_data.csv")

monthly_revenue["month"] = pd.to_datetime(monthly_revenue["month"])
customer_month["month"] = pd.to_datetime(customer_month["month"])

model = joblib.load(BASE_DIR / "models" / "xgb_churn_model.pkl")

# =============================
# COMPUTE METRICS
# =============================

total_revenue = monthly_revenue["total_revenue"].sum()
latest_mrr = monthly_revenue.iloc[-1]["total_revenue"]
total_customers = customer_month["customer_id"].nunique()
churn_rate = customer_month.groupby("customer_id")["churn"].first().mean() * 100

# =============================
# REVENUE TREND FIG
# =============================

fig, ax = plt.subplots(figsize=(10,4), facecolor="#0e1117")
ax.plot(monthly_revenue["month"], monthly_revenue["total_revenue"], linewidth=2)
ax.set_facecolor("#0e1117")
ax.grid(alpha=0.2)
ax.tick_params(colors='white')
for spine in ax.spines.values():
    spine.set_color('#444')
plt.xticks(rotation=45)

# =============================
# FORECAST FIG
# =============================

monthly_revenue["growth_rate"] = monthly_revenue["total_revenue"].pct_change()
avg_growth = monthly_revenue["growth_rate"].median()

forecast_months = 6
last_value = monthly_revenue["total_revenue"].iloc[-1]

future_values = []
current_value = last_value

for _ in range(forecast_months):
    current_value *= (1 + avg_growth)
    future_values.append(current_value)

future_dates = pd.date_range(
    start=monthly_revenue["month"].iloc[-1],
    periods=forecast_months + 1,
    freq="MS"
)[1:]

forecast_df = pd.DataFrame({
    "month": future_dates,
    "total_revenue": future_values
})

fig2, ax2 = plt.subplots(figsize=(10,4), facecolor="#0e1117")
ax2.plot(monthly_revenue["month"], monthly_revenue["total_revenue"], label="Historical", linewidth=2)
ax2.plot(forecast_df["month"], forecast_df["total_revenue"], linestyle="--", label="Forecast")
ax2.set_facecolor("#0e1117")
ax2.grid(alpha=0.2)
ax2.legend()
ax2.tick_params(colors='white')
for spine in ax2.spines.values():
    spine.set_color('#444')
plt.xticks(rotation=45)

# =============================
# AI RISK ENGINE
# =============================

customer_features = customer_month.groupby("customer_id").agg({
    "login_count": "mean",
    "feature_usage_score": "mean",
    "ticket_count": "mean",
    "payment_delay_days": "mean",
    "amount_paid": "sum",
    "churn": "first"
}).reset_index()

customer_features.rename(columns={
    "login_count": "avg_login",
    "feature_usage_score": "avg_feature_usage",
    "ticket_count": "avg_ticket_count",
    "payment_delay_days": "avg_payment_delay",
    "amount_paid": "total_revenue"
}, inplace=True)

X_live = customer_features.drop(columns=["customer_id", "churn"])
X_live = X_live.reindex(columns=model.get_booster().feature_names, fill_value=0)

customer_features["churn_probability"] = model.predict_proba(X_live)[:,1]

customer_features["risk_level"] = pd.cut(
    customer_features["churn_probability"],
    bins=[0, 0.3, 0.6, 1],
    labels=["Low", "Medium", "High"]
)

high_risk = customer_features[customer_features["risk_level"] == "High"]

revenue_at_risk = (
    high_risk["total_revenue"] * high_risk["churn_probability"]
).sum()

risk_percentage = (revenue_at_risk / total_revenue) * 100

# Risk distribution
risk_counts = (
    customer_features["risk_level"]
    .value_counts()
    .reindex(["Low", "Medium", "High"])
)

fig3, ax3 = plt.subplots(figsize=(6,4), facecolor="#0e1117")
risk_counts.plot(kind="bar", ax=ax3)
ax3.set_facecolor("#0e1117")
ax3.grid(axis="y", alpha=0.2)
ax3.tick_params(colors='white')
for spine in ax3.spines.values():
    spine.set_color('#444')

# Top customers
top_risk = customer_features.sort_values(
    by="churn_probability",
    ascending=False
).head(20)

top_risk_display = top_risk.copy()
top_risk_display["churn_probability"] = (
    top_risk_display["churn_probability"]
    .astype(float)
    .mul(100)
    .round(2)
)

top_risk_display["churn_probability"] = (
    top_risk_display["churn_probability"]
    .apply(lambda x: f"{x:.2f}%")
)

top_risk_display["total_revenue"] = top_risk_display["total_revenue"].apply(lambda x: f"₹{x:,.0f}")

# =============================
# PAGE ROUTING DISPLAY
# =============================

if page == "Home":

    col1, col2 = st.columns([1,1])

    with col1:
        st.markdown("""
        <h1 style='font-size:48px;'> AI Revenue Intelligence Platform</h1>
        <p style='font-size:20px; color:#9ca3af;'>
        Transforming SaaS Data into Predictive Business Intelligence
        </p>
        """, unsafe_allow_html=True)

    with col2:
        lottie_ai = load_lottie(
            "https://assets5.lottiefiles.com/packages/lf20_kyu7xb1v.json"
        )
        st_lottie(lottie_ai, height=300)

    st.markdown("---")

    # =============================
    # PROJECT SUMMARY
    # =============================


    glass_section(" Project Overview")

    st.markdown("""
    -  Revenue modeling  
    -  AI churn prediction  
    -  Revenue risk quantification  
    -  Forecasting engine  
    """)

    st.markdown("</div>", unsafe_allow_html=True)

    # =============================
    # MODEL PERFORMANCE SECTION
    # =============================

    st.markdown("## Model Performance")

    col1, col2, col3 = st.columns(3)

    col1.metric("ROC-AUC Score", "0.78")
    col2.metric("Recall (Churn Focused)", "83%")
    col3.metric("Model Type", "XGBoost")

    st.markdown("""
    • Optimized for **Recall** to capture high-risk churn customers  
    • Balanced against acceptable precision  
    • Feature importance validation applied  
    """)

    st.markdown("---")

    # =============================
    # BUSINESS IMPACT SECTION
    # =============================

    st.markdown("##  AI-Driven Revenue Protection")

    estimated_retention_gain = revenue_at_risk * 0.30

    col1, col2 = st.columns(2)

    col1.metric(
        "Revenue Currently Exposed",
        f"₹{revenue_at_risk:,.0f}"
    )

    col2.metric(
        "Revenue Recoverable (30% Intervention)",
        f"₹{estimated_retention_gain:,.0f}"
    )

    st.info("Predictive AI enables proactive customer retention strategies, directly improving profitability.")

    # =============================
    # ARCHITECTURE DIAGRAM
    # =============================

    st.markdown("##  Interactive System Architecture")

    st.graphviz_chart("""
    digraph {
        node [shape=box, style="filled", color="#1f2937", fontcolor="white"];
        
        A [label="Raw SaaS Data"];
        B [label="Data Cleaning & Feature Engineering"];
        C [label="XGBoost Model"];
        D [label="Churn Probability Engine"];
        E [label="Revenue Risk Calculator"];
        F [label="Streamlit Intelligence Dashboard"];

        A -> B -> C -> D -> E -> F;
    }
    """)

    st.markdown("---")

    # =============================
    # LIVE DEMO EXPLANATION
    # =============================

    st.markdown("##  How to Use This Platform")

    st.markdown("""
    1️⃣ Navigate to **Executive Overview** → Business KPIs  
    2️⃣ View **Revenue Analytics** → Growth trajectory  
    3️⃣ Open **Forecasting** → Future revenue projections  
    4️⃣ Explore **Risk Intelligence** → Revenue exposure modeling  
    5️⃣ Review **Customer Insights** → AI churn predictions  

    This simulates how leadership teams monitor SaaS health in real-time.
    """)

    st.markdown("---")

    st.success("Use the sidebar to explore each intelligence module.")
elif page == "Executive Overview":

    st.markdown("##  Executive Metrics")

    col1, col2, col3, col4 = st.columns(4)

    kpi1 = col1.empty()
    kpi2 = col2.empty()
    kpi3 = col3.empty()
    kpi4 = col4.empty()

    for i in range(0, 101, 5):
        kpi1.metric(" Total Revenue", f"₹{int(total_revenue * i / 100):,}")
        kpi2.metric(" Latest MRR", f"₹{int(latest_mrr * i / 100):,}")
        kpi3.metric(" Total Customers", f"{int(total_customers * i / 100):,}")
        kpi4.metric(" Churn Rate", f"{churn_rate * i / 100:.2f}%")
        time.sleep(0.02)

elif page == "Revenue Analytics":

    st.markdown("##  Revenue Performance")
    st.pyplot(fig)

elif page == "Forecasting":

    st.markdown("##  Revenue Forecast (Next 6 Months)")
    st.pyplot(fig2)

elif page == "Risk Intelligence":

    st.markdown("##  AI Risk Intelligence Engine")

    st.metric(
        " Revenue At Risk",
        f"₹{revenue_at_risk:,.0f}",
        f"{risk_percentage:.2f}% of Total Revenue"
    )

    st.pyplot(fig3)

elif page == "Customer Insights":

    st.markdown("##  Top 20 High-Risk Customers")

    st.dataframe(
        top_risk_display[[
            "customer_id",
            "total_revenue",
            "churn_probability",
            "risk_level"
        ]],
        use_container_width=True
    )
st.markdown("""
<div class="footer">
Built & Designed by <b>Gokul B</b> · AI & Data Intelligence Engineer · 2026
</div>
""", unsafe_allow_html=True)
