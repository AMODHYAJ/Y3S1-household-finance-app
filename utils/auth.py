# utils/auth.py
import streamlit as st

def check_password():
    """Returns `True` if the user entered the correct password."""
    if 'password' not in st.session_state:
        st.session_state.password = None

    if st.session_state.password == 'finance123':  # Simple default password
        return True

    password_input = st.sidebar.text_input("Enter Password", type="password")
    if password_input:
        if password_input == 'finance123':
            st.session_state.password = password_input
            st.rerun()
        else:
            st.sidebar.error("😕 Password incorrect")
    return False

def check_fairness(transactions_df):
    """Basic fairness check - ensure no category dominates spending excessively"""
    expense_ratios = transactions_df[transactions_df['Type'] == 'Expense'].groupby('Category')['Amount'].sum() / transactions_df['Amount'].sum()
    if any(ratio > 0.5 for ratio in expense_ratios):  # If any category > 50%
        return "Warning: Over-reliance on one spending category detected"
    return "Spending distribution appears balanced"