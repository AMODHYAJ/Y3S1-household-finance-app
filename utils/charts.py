# utils/charts.py
import plotly.express as px
import pandas as pd

def create_expense_pie_chart(transactions_df):
    """Creates a pie chart of expenses by category"""
    expense_df = transactions_df[transactions_df['Type'] == 'Expense']
    if expense_df.empty:
        return None
        
    chart_data = expense_df.groupby('Category')['Amount'].sum().reset_index()
    fig = px.pie(chart_data, values='Amount', names='Category', 
                 title='Where Your Money Goes', hole=0.3)
    return fig

def create_cashflow_trend_chart(transactions_df):
    """Creates a line chart of income vs expenses over time"""
    if transactions_df.empty:
        return None

    transactions_df['Date'] = pd.to_datetime(transactions_df['Date'])
    transactions_df['Month'] = transactions_df['Date'].dt.to_period('M').astype(str)
    
    monthly_data = transactions_df.groupby(['Month', 'Type'])['Amount'].sum().reset_index()
    pivot_df = monthly_data.pivot(index='Month', columns='Type', values='Amount').fillna(0)
    
    fig = px.line(pivot_df, x=pivot_df.index, y=['Income', 'Expense'],
                 title='Monthly Income vs Expenses Trend',
                 labels={'value': 'Amount ($)', 'variable': 'Type', 'index': 'Month'})
    return fig