# pages/1_🏠_Dashboard.py
import streamlit as st
import pandas as pd
from utils.data_loader import load_transactions, load_goals
from utils.charts import create_expense_pie_chart, create_cashflow_trend_chart
from utils.insight_agent import generate_financial_insights

st.set_page_config(layout="wide")
st.title("🏠 Financial Dashboard")
st.markdown("## Your Complete Financial Overview")

# Load the data using your Data Loader agent
transaction_df = load_transactions()
goals_df = load_goals()

# Calculate key metrics
if not transaction_df.empty:
    total_income = transaction_df[transaction_df['Type'] == 'Income']['Amount'].sum()
    total_expenses = transaction_df[transaction_df['Type'] == 'Expense']['Amount'].sum()
    net_cashflow = total_income - total_expenses
else:
    total_income = total_expenses = net_cashflow = 0.0

# Display metrics in columns
col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"${total_income:,.2f}")
col2.metric("Total Expenses", f"${total_expenses:,.2f}")
col3.metric("Net Cash Flow", f"${net_cashflow:,.2f}", 
            delta=f"{net_cashflow:,.2f}")

# Create charts section
st.divider()
st.header("📊 Financial Analysis")

if not transaction_df.empty:
    # Create two columns for the charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Expense Breakdown")
        pie_fig = create_expense_pie_chart(transaction_df)
        if pie_fig:
            st.plotly_chart(pie_fig, use_container_width=True)
        else:
            st.info("No expenses to chart.")
            
    with col2:
        st.subheader("Cash Flow Trend")
        trend_fig = create_cashflow_trend_chart(transaction_df)
        if trend_fig:
            st.plotly_chart(trend_fig, use_container_width=True)
        else:
            st.info("Not enough data for trend analysis.")
else:
    st.info("Add some transactions to see charts here!")

# Show raw data for debugging (you can remove this later)
st.subheader("Raw Data Preview")
st.dataframe(transaction_df)

# AI Insights Section
st.divider()
st.header("💡 AI-Powered Insights")

if st.button("🧠 Analyze My Finances", type="primary"):
    with st.spinner("Thinking..."):
        insights = generate_financial_insights(transaction_df, goals_df)
    st.success("Here's your financial health analysis:")
    st.write(insights)
