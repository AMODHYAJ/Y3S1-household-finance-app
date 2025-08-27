# pages/2_💸_Add_Expense.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("💸 Add an Expense")
st.markdown("Track your spending here.")

# Create a form for user input
with st.form("expense_form", clear_on_submit=True):
    date = st.date_input("Date")
    description = st.text_input("What did you spend money on?")
    amount = st.number_input("Amount ($)", min_value=0.0, step=0.01)
    category = st.selectbox("Category", ["🍔 Food & Dining", "🛒 Shopping", "🏠 Rent & Utilities", "⛽ Transportation", "🎉 Entertainment", "🧾 Other"])
    
    # Submit button
    submitted = st.form_submit_button("Save Expense")

# Check if the form was submitted
if submitted:
    # Create a dictionary for the new transaction
    new_expense = {
        "Date": [date],
        "Description": [description],
        "Amount": [amount],
        "Category": [category]
    }
    
    # Create a DataFrame from the new transaction
    new_expense_df = pd.DataFrame(new_expense)
    
    # Try to read existing data, if not, create a new DataFrame
    try:
        expenses_df = pd.read_csv('expenses.csv')
        updated_df = pd.concat([expenses_df, new_expense_df], ignore_index=True)
    except FileNotFoundError:
        updated_df = new_expense_df
        
    # Save back to CSV
    updated_df.to_csv('expenses.csv', index=False)
    st.success(f"✅ Added ${amount:.2f} for {description}!")

    # Try to display a simple chart
try:
    expenses_df = pd.read_csv('expenses.csv')
    if not expenses_df.empty:
        st.divider()
        st.subheader("Your Spending Breakdown")
        
        # Group by category and sum the amount
        chart_data = expenses_df.groupby('Category')['Amount'].sum().reset_index()
        
        # Create a pie chart
        fig = px.pie(chart_data, values='Amount', names='Category', title='Where Your Money Went')
        st.plotly_chart(fig, use_container_width=True)
except FileNotFoundError:
    st.info("Add an expense to see a chart here!")
