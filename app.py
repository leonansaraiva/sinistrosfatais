import streamlit as st
from login import is_logged_in, login_callback, logout_callback, show_login
from dashboard import show_dashboard

import streamlit as st
from mapa import show_map

st.set_page_config(layout="wide")

def main():
    if is_logged_in():
        show_dashboard(logout_callback)
    else:
        show_login(login_callback)

if __name__ == "__main__":
    main()
