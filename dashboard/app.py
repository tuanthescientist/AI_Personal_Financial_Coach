"""
AI Personal Financial Coach — Streamlit Dashboard
───────────────────────────────────────────────────
Interactive web UI for monitoring spending, chatting with the AI coach,
and viewing product recommendations.
"""

import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

API_BASE = "http://localhost:8000/api/v1"

st.set_page_config(
    page_title="AI Financial Coach · SOL",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Sidebar ───────────────────────────────────────────
st.sidebar.title("💰 SOL Financial Coach")
user_id = st.sidebar.text_input("User ID", value="demo_user_001")
days = st.sidebar.slider("Analysis period (days)", 7, 90, 30)

st.sidebar.markdown("---")
st.sidebar.markdown("**Powered by Google Gemini**")

# ── Main Content ──────────────────────────────────────
tab_overview, tab_chat, tab_recommend = st.tabs(
    ["📊 Spending Overview", "💬 AI Coach Chat", "🎯 Recommendations"]
)

# ─────────────────────────── TAB 1: Overview ──────────
with tab_overview:
    st.header("Spending & Income Analysis")

    try:
        resp = requests.get(f"{API_BASE}/spending/{user_id}", params={"days": days}, timeout=10)
        if resp.status_code == 200:
            data = resp.json()

            # KPI row
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Income", f"{data['total_income']:,.0f} ₫")
            col2.metric("Total Expenses", f"{data['total_expenses']:,.0f} ₫")
            col3.metric("Net Savings", f"{data['net_savings']:,.0f} ₫",
                        delta=f"{data['savings_rate']:.0%}")
            col4.metric("Savings Rate", f"{data['savings_rate']:.0%}")

            st.markdown("---")

            # Charts
            chart_col1, chart_col2 = st.columns(2)

            with chart_col1:
                cat_df = pd.DataFrame(data["categories"])
                if not cat_df.empty:
                    fig_pie = px.pie(
                        cat_df, values="amount", names="category",
                        title="Expense Breakdown by Category",
                        hole=0.4,
                        color_discrete_sequence=px.colors.qualitative.Set2,
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)

            with chart_col2:
                if not cat_df.empty:
                    fig_bar = px.bar(
                        cat_df.sort_values("amount", ascending=True),
                        x="amount", y="category", orientation="h",
                        title="Spending by Category (VND)",
                        color="percentage",
                        color_continuous_scale="RdYlGn_r",
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)

            # Savings gauge
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=data["savings_rate"] * 100,
                title={"text": "Savings Rate (%)"},
                gauge={
                    "axis": {"range": [0, 50]},
                    "bar": {"color": "#2ecc71"},
                    "steps": [
                        {"range": [0, 10], "color": "#e74c3c"},
                        {"range": [10, 20], "color": "#f39c12"},
                        {"range": [20, 50], "color": "#27ae60"},
                    ],
                },
            ))
            st.plotly_chart(fig_gauge, use_container_width=True)

            # Insights
            st.subheader("💡 Insights")
            for insight in data.get("insights", []):
                st.info(insight)
            for anomaly in data.get("anomalies", []):
                st.warning(anomaly)
        else:
            st.error(f"API error: {resp.status_code}")
    except requests.ConnectionError:
        st.warning("Cannot connect to backend API. Make sure the FastAPI server is running on port 8000.")

# ─────────────────────────── TAB 2: Chat ──────────────
with tab_chat:
    st.header("Chat with your AI Financial Coach")

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask a financial question…"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                try:
                    resp = requests.post(
                        f"{API_BASE}/chat/",
                        json={"user_id": user_id, "message": prompt},
                        timeout=30,
                    )
                    if resp.status_code == 200:
                        answer = resp.json()["response"]
                        st.markdown(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    else:
                        st.error(f"API error {resp.status_code}")
                except requests.ConnectionError:
                    st.error("Backend not reachable.")

# ─────────────────────────── TAB 3: Recommendations ───
with tab_recommend:
    st.header("🎯 Personalised Product Recommendations")

    if st.button("Generate Recommendations"):
        with st.spinner("Analysing your profile…"):
            try:
                resp = requests.get(f"{API_BASE}/recommendations/{user_id}", timeout=30)
                if resp.status_code == 200:
                    recs = resp.json()
                    if recs:
                        for r in recs:
                            with st.container():
                                st.subheader(f"{r.get('product_name', 'Product')}")
                                st.caption(f"Type: {r.get('product_type', '')} · Priority: {r.get('priority', 'medium')}")
                                st.progress(r.get("confidence_score", 0.5))
                                st.write(r.get("reason", ""))
                                st.markdown("---")
                    else:
                        st.info("No recommendations at this time.")
                else:
                    st.error(f"API error {resp.status_code}")
            except requests.ConnectionError:
                st.error("Backend not reachable.")
