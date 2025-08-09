import streamlit as st
import time
import gspread
import pandas as pd
import numpy as np
from google.oauth2.service_account import Credentials

st.set_page_config(layout="wide")

SESSION_TIMEOUT_MINUTES = 10

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_time" not in st.session_state:
    st.session_state.login_time = 0
if "login_failed" not in st.session_state:
    st.session_state.login_failed = False

def get_scopes():
    return [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

def is_logged_in():
    if not st.session_state.get("logged_in", False):
        return False
    if time.time() - st.session_state.get("login_time", 0) > SESSION_TIMEOUT_MINUTES * 60:
        st.session_state.logged_in = False
        return False
    return True

def login_callback():
    user = st.session_state.get("user_input", "")
    pwd = st.session_state.get("password_input", "")
    if user == st.secrets["APP_USER"] and pwd == st.secrets["APP_PASSWORD"]:
        st.session_state.logged_in = True
        st.session_state.login_time = time.time()
        st.session_state.login_failed = False
    else:
        st.session_state.logged_in = False
        st.session_state.login_failed = True

def logout_callback():
    st.session_state.logged_in = False
    st.session_state.login_failed = False
    st.session_state.user_input = ""
    st.session_state.password_input = ""
    st.query_params = {"logout": str(time.time())}
    st.rerun()

def get_google_sheet_data():
    creds = Credentials.from_service_account_info(
        st.secrets["google_service_account"],
        scopes=get_scopes()
    )
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(st.secrets["SHEET_ID"])
    sheet = spreadsheet.worksheet("dados")
    records = sheet.get_all_records()
    df = pd.DataFrame(records)

    if "Número (KM)" in df.columns:
        df["Número (KM)"] = df["Número (KM)"].replace('-', np.nan)
        df["Número (KM)"] = pd.to_numeric(df["Número (KM)"], errors='coerce')

    return df

def show_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            """
            <div style="max-width: 400px; margin: auto;">
            """,
            unsafe_allow_html=True
        )
        st.title("Login")
        st.text_input("Usuário", key="user_input")
        st.text_input("Senha", type="password", key="password_input")
        st.button("Entrar", on_click=login_callback)
        if st.session_state.get("login_failed", False):
            st.error("Usuário ou senha inválidos")
        st.markdown("</div>", unsafe_allow_html=True)

def show_protected_content():
    st.success("Você está logado!")
    with st.spinner("Carregando dados da planilha..."):
        data = get_google_sheet_data()
    st.dataframe(data, use_container_width=True, height=800)

    if st.button("Logout"):
        logout_callback()

def main():
    if is_logged_in():
        show_protected_content()
    else:
        show_login()

if __name__ == "__main__":
    main()
