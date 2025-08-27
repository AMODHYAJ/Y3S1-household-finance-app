# pages/3_💰_Add_Income.py
import streamlit as st
import pandas as pd

st.title("💰 Add Income")

with st.form("income_form", clear_on_submit=True):
    date = st.date_input("Date")
    description = st.text_input("Source", placeholder="e.g., Salary, Freelance, Gift")
    amount = st.number_input("Amount ($)", min_value=0.0, step=0.01)
    category = st.selectbox("Category", ["💼 Salary", "🤝 Freelance", "🎁 Gift", "📈 Investment", "🧾 Other"])
    submitted = st.form_submit_button("Save Income")

def sanitize_input(input_text):
    """Basic input sanitization"""
    import re
    # Remove potentially harmful characters
    return re.sub(r'[;\\/*\']', '', str(input_text))

if submitted:
    description = sanitize_input(description)
    new_income = {
        "Date": date,
        "Description": description,
        "Amount": amount,
        "Category": category
    }
    
    new_income_df = pd.DataFrame([new_income])
    
    try:
        existing_df = pd.read_csv('income.csv')
        updated_df = pd.concat([existing_df, new_income_df], ignore_index=True)
    except FileNotFoundError:
        updated_df = new_income_df
        
    updated_df.to_csv('income.csv', index=False)
    st.success(f"✅ Saved ${amount:.2f} from {description}!")