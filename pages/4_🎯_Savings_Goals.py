# pages/4_🎯_Savings_Goals.py
import streamlit as st
import pandas as pd
from utils.data_loader import load_transactions

st.title("🎯 Savings Goals")

# Load transactions to calculate available funds
transaction_df = load_transactions()
if not transaction_df.empty:
    total_income = transaction_df[transaction_df['Type'] == 'Income']['Amount'].sum()
    total_expenses = transaction_df[transaction_df['Type'] == 'Expense']['Amount'].sum()
    available_funds = total_income - total_expenses
else:
    available_funds = 0

# Display available funds
st.subheader(f"Available Funds: ${available_funds:,.2f}")

# Form to Set New Goal
with st.form("goal_form", clear_on_submit=True):
    goal_name = st.text_input("Goal Name", placeholder="e.g., New Laptop, Vacation")
    target_amount = st.number_input("Target Amount ($)", min_value=1.0, step=1.0)
    deadline = st.date_input("Goal Deadline")
    submitted = st.form_submit_button("Save Goal")

# Initialize goals_df to avoid reference before assignment
goals_df = pd.DataFrame()

if submitted:
    new_goal = {
        "Goal": [goal_name],
        "Target": [target_amount],
        "Deadline": [deadline],
        "Saved": [0.0]
    }
    
    new_goal_df = pd.DataFrame(new_goal)
    
    try:
        goals_df = pd.read_csv('savings_goals.csv')
        # Ensure both DataFrames have the same columns before concatenation
        if not goals_df.empty:
            updated_df = pd.concat([goals_df, new_goal_df], ignore_index=True)
        else:
            updated_df = new_goal_df
    except FileNotFoundError:
        updated_df = new_goal_df
        
    updated_df.to_csv('savings_goals.csv', index=False)
    st.success(f"✅ Goal '{goal_name}' saved!")
    st.rerun()

# Display Existing Goals
try:
    goals_df = pd.read_csv('savings_goals.csv')
    # Ensure the DataFrame has the expected columns
    expected_columns = ['Goal', 'Target', 'Deadline', 'Saved']
    for col in expected_columns:
        if col not in goals_df.columns:
            goals_df[col] = 0.0 if col == 'Saved' else '' if col == 'Goal' else pd.NaT if col == 'Deadline' else 0.0
    
    if not goals_df.empty:
        st.divider()
        st.subheader("Your Goals")
        
        for index, row in goals_df.iterrows():
            with st.container(border=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader(f"{row['Goal']}")
                    st.write(f"**Target:** ${row['Target']:,.2f}")
                    st.write(f"**Deadline:** {row['Deadline']}")
                    st.write(f"**Saved:** ${row['Saved']:,.2f}")
                with col2:
                    progress = row['Saved'] / row['Target'] if row['Target'] > 0 else 0
                    st.progress(min(progress, 1.0), text=f"{min(progress, 1.0)*100:.0f}%")
                    if progress >= 1.0:
                        st.success("🎉 Goal achieved!")
                    elif progress > 0.75:
                        st.info("🔥 You're getting close!")
                    elif progress > 0:
                        st.write("💪 You're on your way!")
                    else:
                        st.warning("⏰ You haven't started saving yet.")
except FileNotFoundError:
    st.info("⏳ You haven't set any goals yet. Create one above!")
    goals_df = pd.DataFrame(columns=['Goal', 'Target', 'Deadline', 'Saved'])
except Exception as e:
    st.error(f"Error loading goals: {e}")
    goals_df = pd.DataFrame(columns=['Goal', 'Target', 'Deadline', 'Saved'])

# After displaying existing goals, add a contribution section
if not goals_df.empty and available_funds > 0:
    st.divider()
    st.subheader("Contribute to Your Goals")
    
    goal_to_contribute = st.selectbox("Select Goal", goals_df['Goal'].tolist())
    
    # Calculate maximum possible contribution
    goal_index = goals_df[goals_df['Goal'] == goal_to_contribute].index[0]
    remaining_goal = goals_df.at[goal_index, 'Target'] - goals_df.at[goal_index, 'Saved']
    max_contribution = min(available_funds, remaining_goal)
    
    contribution_amount = st.number_input(
        "Contribution Amount ($)", 
        min_value=0.0, 
        max_value=max_contribution,
        step=1.0,
        help=f"Maximum you can contribute: ${max_contribution:,.2f}"
    )
    
    if st.button("Add Contribution"):
        if contribution_amount > available_funds:
            st.error("❌ Contribution amount exceeds available funds!")
        elif contribution_amount > remaining_goal:
            st.error("❌ Contribution amount exceeds remaining goal amount!")
        else:
            # Update the goal with the contribution
            goals_df.at[goal_index, 'Saved'] += contribution_amount
            goals_df.to_csv('savings_goals.csv', index=False)
            
            # Record this as a savings transaction
            try:
                savings_df = pd.read_csv('savings_transactions.csv')
            except FileNotFoundError:
                savings_df = pd.DataFrame(columns=['Date', 'Goal', 'Amount', 'Type'])
            
            new_saving = pd.DataFrame({
                'Date': [pd.Timestamp.now().date()],
                'Goal': [goal_to_contribute],
                'Amount': [contribution_amount],
                'Type': ['Contribution']
            })
            
            # Ensure both DataFrames have the same columns before concatenation
            if not savings_df.empty:
                savings_updated = pd.concat([savings_df, new_saving], ignore_index=True)
            else:
                savings_updated = new_saving
                
            savings_updated.to_csv('savings_transactions.csv', index=False)
            
            st.success(f"✅ Added ${contribution_amount:,.2f} to {goal_to_contribute}!")
            st.rerun()
elif not goals_df.empty and available_funds <= 0:
    st.warning("You don't have available funds to contribute to goals. Add more income or reduce expenses.")