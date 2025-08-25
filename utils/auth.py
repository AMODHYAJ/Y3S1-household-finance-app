# utils/auth.py
import streamlit as st

def check_password():
    """Returns `True` if the user entered the correct password."""
    if 'password' not in st.session_state:
        st.session_state.password = None

    if st.session_state.password == 'finance123':  # Simple default password
        return True

    password_input = st.sidebar.text_input("Enter Password", type="password")
    if password_input:
        if password_input == 'finance123':
            st.session_state.password = password_input
            st.rerun()
        else:
            st.sidebar.error("😕 Password incorrect")
    return False