from openai import OpenAI
import streamlit as st
import random
import pandas as pd

# Fallback insights for demo purposes
FALLBACK_INSIGHTS = [
    "• Your biggest spending category is {category}. Consider setting a weekly budget for this.",
    "• Great job maintaining a positive cash flow! Your net savings is ${net_cashflow:.2f}.",
    "• You're spending {percent:.0f}% of your income on {category}. Look for areas to optimize.",
    "• Based on your current savings rate, you're building a good financial foundation.",
    "• You've saved ${total_saved:.2f} towards your goals. Keep up the good work!",
    "• Your savings rate is {savings_rate:.1f}% of income. {savings_advice}",
    "• You have ${available_funds:.2f} available that could be allocated to your savings goals."
]

def load_savings_transactions():
    """Loads savings contributions data."""
    try:
        return pd.read_csv('savings_transactions.csv')
    except FileNotFoundError:
        return pd.DataFrame()

def generate_financial_insights(transactions_df, goals_df):
    """
    Generates AI-powered financial insights with fallback for demo.
    """
    if transactions_df.empty:
        return "Add some income and expenses to get personalized insights!"
    
    # Calculate financial metrics
    total_income = transactions_df[transactions_df['Type'] == 'Income']['Amount'].sum()
    total_expenses = transactions_df[transactions_df['Type'] == 'Expense']['Amount'].sum()
    net_cashflow = total_income - total_expenses
    available_funds = net_cashflow  # Simplified available funds calculation
    
    expense_df = transactions_df[transactions_df['Type'] == 'Expense']
    if not expense_df.empty:
        top_category = expense_df.groupby('Category')['Amount'].sum().idxmax()
        top_category_amount = expense_df.groupby('Category')['Amount'].sum().max()
        percent_of_income = (top_category_amount / total_income * 100) if total_income > 0 else 0
    else:
        top_category = "expenses"
        percent_of_income = 0

    # Calculate savings metrics
    total_saved = goals_df['Saved'].sum() if not goals_df.empty else 0
    savings_rate = (total_saved / total_income * 100) if total_income > 0 else 0
    
    # Determine savings advice based on savings rate
    if savings_rate == 0:
        savings_advice = "It's important to start saving, even a small amount regularly."
    elif savings_rate < 10:
        savings_advice = "Consider increasing your savings rate to at least 10-15% for better financial security."
    elif savings_rate < 20:
        savings_advice = "Good progress! Aim for 20% or more to accelerate your financial goals."
    else:
        savings_advice = "Excellent savings rate! You're building strong financial habits."

    # Try Gemini API if available
    try:
        import google.generativeai as genai
        genai.configure(api_key=st.secrets.get("GEMINI_API_KEY", ""))
        
        # Build more comprehensive prompt with savings data
        prompt = f"""Analyze this financial data as a friendly financial advisor:
        
        INCOME & EXPENSES:
        - Total Income: ${total_income:.2f}
        - Total Expenses: ${total_expenses:.2f}
        - Net Cash Flow: ${net_cashflow:.2f}
        - Available Funds: ${available_funds:.2f}
        - Top Spending Category: {top_category} (${top_category_amount:.2f}, {percent_of_income:.1f}% of income)
        
        SAVINGS & GOALS:
        - Total Saved: ${total_saved:.2f}
        - Savings Rate: {savings_rate:.1f}% of income
        - Number of Goals: {len(goals_df) if not goals_df.empty else 0}
        {f"- Goals: {', '.join(goals_df['Goal'].tolist())}" if not goals_df.empty else ""}
        
        Please provide 3-4 bullet points of concise, actionable advice focusing on:
        1. Spending patterns and optimization opportunities
        2. Savings performance and recommendations
        3. Goal progress and suggestions
        4. Overall financial health assessment
        
        Be encouraging but honest, and provide specific recommendations when possible."""
        
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        # Fallback to predefined insights with savings data
        insights = []
        
        # Add 2-3 random insights from our fallback list
        selected_insights = random.sample(FALLBACK_INSIGHTS, min(3, len(FALLBACK_INSIGHTS)))
        for template in selected_insights:
            try:
                insight = template.format(
                    category=top_category,
                    net_cashflow=net_cashflow,
                    percent=percent_of_income,
                    total_saved=total_saved,
                    savings_rate=savings_rate,
                    savings_advice=savings_advice,
                    available_funds=available_funds
                )
                insights.append(insight)
            except:
                # Skip templates that don't match our parameters
                continue
        
        # Add specific savings insights if we have goals
        if not goals_df.empty:
            if total_saved > 0:
                goal_progress = []
                for _, goal in goals_df.iterrows():
                    progress = (goal['Saved'] / goal['Target']) * 100
                    goal_progress.append(f"{goal['Goal']} ({progress:.1f}%)")
                
                insights.append(f"• Goal progress: {', '.join(goal_progress)}")
            
            # Check if any goals are nearing deadline
            today = pd.Timestamp.now().date()
            for _, goal in goals_df.iterrows():
                deadline = pd.to_datetime(goal['Deadline']).date()
                days_remaining = (deadline - today).days
                if 0 < days_remaining < 30 and goal['Saved'] < goal['Target']:
                    needed = goal['Target'] - goal['Saved']
                    insights.append(f"• ⚠️ {goal['Goal']} deadline in {days_remaining} days! You need ${needed:.2f} more.")
        
        return "💡 Financial Insights:\n\n" + "\n".join(insights)