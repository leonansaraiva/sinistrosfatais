import streamlit as st
import time
import gspread
from google.oauth2.service_account import Credentials

SESSION_TIMEOUT_MINUTES = 10

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.login_time = 0
    st.session_state.login_failed = False

def is_logged_in():
    if not st.session_state.logged_in:
        return False
    if time.time() - st.session_state.login_time > SESSION_TIMEOUT_MINUTES * 60:
        st.session_state.logged_in = False
        return False
    return True

def login_callback():
    user = st.session_state.user_input
    pwd = st.session_state.password_input
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

if not is_logged_in():
    st.title("Login")
    st.text_input("Usuário", key="user_input")
    st.text_input("Senha", type="password", key="password_input")
    st.button("Entrar", on_click=login_callback)
    if st.session_state.login_failed:
        st.error("Usuário ou senha inválidos")
else:
    st.success("Você está logado!")
    st.write("Conteúdo protegido aqui...")

    # Ler dados do Google Sheets
    with st.spinner("Carregando dados da planilha..."):
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = Credentials.from_service_account_info(
            st.secrets["google_service_account"],
            scopes=scopes
        )
        client = gspread.authorize(creds)

        spreadsheet = client.open_by_key(st.secrets["SHEET_ID"])
        sheet = spreadsheet.worksheet("dados")
        data = sheet.get_all_records()

    st.dataframe(data, use_container_width=True)

    st.button("Logout", on_click=logout_callback)
