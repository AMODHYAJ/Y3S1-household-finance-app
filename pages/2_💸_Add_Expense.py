# pages/2_💸_Add_Expense.py
import streamlit as st
import pandas as pd

st.title("💸 Add an Expense")

with st.form("expense_form", clear_on_submit=True):
    date = st.date_input("Date")
    description = st.text_input("What did you spend on?")
    amount = st.number_input("Amount ($)", min_value=0.0, step=0.01)
    category = st.selectbox("Category", ["🍔 Food", "🏠 Rent", "⛽ Transport", "🎉 Entertainment", "🧾 Other"])
    submitted = st.form_submit_button("Save Expense")

def sanitize_input(input_text):
    """Basic input sanitization"""
    import re
    # Remove potentially harmful characters
    return re.sub(r'[;\\/*\']', '', str(input_text))

if submitted:
    description = sanitize_input(description)
    new_expense = {
        "Date": date,
        "Description": description,
        "Amount": amount,
        "Category": category
    }
    
    new_expense_df = pd.DataFrame([new_expense])
    
    try:
        existing_df = pd.read_csv('expenses.csv')
        updated_df = pd.concat([existing_df, new_expense_df], ignore_index=True)
    except FileNotFoundError:
        updated_df = new_expense_df
        
    updated_df.to_csv('expenses.csv', index=False)
    st.success(f"✅ Saved ${amount:.2f} for {description}!")