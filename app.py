import streamlit as st
from utils.auth import check_password

# Set page title and layout
st.set_page_config(page_title="Finance Guru", page_icon="💸", layout="wide")

# Check password - if wrong, stops the app
if not check_password():
    st.stop()

# If password is correct, show the main app
st.title("🏠 Welcome to Your Financial Dashboard!")
st.markdown("""
Use the sidebar on the left to navigate through the app.
*   **Dashboard:** See your overall financial health report.
*   **Add Expense:** Log a new purchase.
*   **Add Income:** Log new money received.
*   **Savings Goals:** Set and track your financial goals.
""")