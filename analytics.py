import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Connect to database
engine = create_engine("sqlite:///smartpay.db")

st.title("💳 SmartPay Analytics Dashboard")

# Load transactions
df = pd.read_sql("SELECT * FROM transactions", engine)

if df.empty:
    st.warning("No transactions found.")
else:
    # ---- KPIs ----
    total_txns = len(df)
    total_fraud = df["fraud_flag"].sum()
    fraud_rate = (total_fraud / total_txns) * 100

    st.subheader("📊 Key Metrics")
    st.write(f"Total Transactions: {total_txns}")
    st.write(f"Fraud Transactions: {total_fraud}")
    st.write(f"Fraud Rate: {fraud_rate:.2f}%")

    # ---- Risk Distribution ----
    st.subheader("⚠ Risk Score Distribution")
    st.bar_chart(df["risk_score"])

    # ---- Transaction Amount Chart ----
    st.subheader("💰 Transaction Amounts")
    st.line_chart(df["amount"])
