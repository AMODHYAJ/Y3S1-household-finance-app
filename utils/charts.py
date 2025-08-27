# utils/charts.py
import plotly.express as px
import pandas as pd
from utils.data_loader import load_transaction_data

def create_cashflow_chart():
    """Creates a bar chart of Monthly Income vs Expenses"""
    df = load_transaction_data()
    if df.empty:
        return None
        
    # Convert Date to datetime and extract year-month
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year-Month'] = df['Date'].dt.to_period('M').astype(str)
    
    # Pivot the data to get income and expense totals per month
    summary_df = df.groupby(['Year-Month', 'Type'])['Amount'].sum().reset_index()
    pivot_df = summary_df.pivot(index='Year-Month', columns='Type', values='Amount').fillna(0)
    
    # Create the bar chart
    fig = px.bar(pivot_df, x=pivot_df.index, y=['Income', 'Expense'],
                 title="Monthly Income vs Expenses",
                 labels={'value': 'Amount ($)', 'variable': 'Type', 'index': 'Month'})
    return fig