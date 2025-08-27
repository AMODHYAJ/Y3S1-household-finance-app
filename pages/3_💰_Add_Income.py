# pages/3_💰_Add_Income.py
import streamlit as st
import pandas as pd

st.title("💰 Add Income")
st.markdown("Log your salary, bonuses, and other money you receive.")

with st.form("income_form", clear_on_submit=True):
    date = st.date_input("Date")
    description = st.text_input("Source of Income", placeholder="e.g., Salary, Freelancing, Gift")
    amount = st.number_input("Amount ($)", min_value=0.0, step=0.01)
    category = st.selectbox("Category", ["💼 Salary", "🤝 Freelance", "🎁 Gift", "📈 Investment", "🧾 Other"])
    
    submitted = st.form_submit_button("Save Income")

if submitted:
    new_income = {
        "Date": [date],
        "Description": [description],
        "Amount": [amount],
        "Category": [category]
    }
    
    new_income_df = pd.DataFrame(new_income)
    
    try:
        income_df = pd.read_csv('income.csv')
        updated_df = pd.concat([income_df, new_income_df], ignore_index=True)
    except FileNotFoundError:
        updated_df = new_income_df
        
    updated_df.to_csv('income.csv', index=False)
    st.success(f"✅ Added ${amount:.2f} from {description}!")