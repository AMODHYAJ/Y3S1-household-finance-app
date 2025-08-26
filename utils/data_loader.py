# utils/data_loader.py
import pandas as pd
import streamlit as st

def load_transactions():
    """
    Loads and combines all transaction data from CSV files.
    Returns a DataFrame with columns: Date, Description, Amount, Type, Category.
    """
    data_frames = []
    
    # Try to load expenses
    try:
        expenses_df = pd.read_csv('expenses.csv')
        expenses_df['Type'] = 'Expense'  # Add a Type column
        data_frames.append(expenses_df)
    except FileNotFoundError:
        st.sidebar.info("No expenses data found.")
    
    # Try to load income
    try:
        income_df = pd.read_csv('income.csv')
        income_df['Type'] = 'Income'  # Add a Type column
        data_frames.append(income_df)
    except FileNotFoundError:
        st.sidebar.info("No income data found.")
    
    # Combine all data
    if data_frames:
        master_df = pd.concat(data_frames, ignore_index=True)
        # Convert date column to datetime
        if 'Date' in master_df.columns:
            master_df['Date'] = pd.to_datetime(master_df['Date']).dt.date
        return master_df
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no files exist

def load_goals():
    """Loads savings goals data from a CSV file."""
    try:
        return pd.read_csv('savings_goals.csv')
    except FileNotFoundError:
        return pd.DataFrame()  # Return an empty DataFrame