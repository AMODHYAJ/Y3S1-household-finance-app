# pages/1_🏠_Dashboard.py
import streamlit as st
import pandas as pd
from utils.data_loader import load_transactions, load_goals

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
st.subheader("Spending Analysis")

if not transaction_df.empty:
    # Expense breakdown chart
    expense_df = transaction_df[transaction_df['Type'] == 'Expense']
    if not expense_df.empty:
        category_totals = expense_df.groupby('Category')['Amount'].sum()
        st.bar_chart(category_totals)
else:
    st.info("Add some transactions to see charts here!")

# Show raw data for debugging (you can remove this later)
st.subheader("Raw Data Preview")
st.dataframe(transaction_df)

