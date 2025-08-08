import streamlit as st
import time
import gspread
from google.oauth2.service_account import Credentials

SESSION_TIMEOUT_MINUTES = 10

def is_logged_in():
    if "logged_in" not in st.session_state:
        return False
    if not st.session_state.logged_in:
        return False
    login_time = st.session_state.get("login_time", 0)
    if time.time() - login_time > SESSION_TIMEOUT_MINUTES * 60:
        st.session_state.logged_in = False
        return False
    return True

def do_login(user, password):
    if user == st.secrets["APP_USER"] and password == st.secrets["APP_PASSWORD"]:
        st.session_state.logged_in = True
        st.session_state.login_time = time.time()
        return True
    return False

def logout():
    st.session_state.logged_in = False

if not is_logged_in():
    st.title("Login")
    user = st.text_input("Usuário", key="user_input")
    password = st.text_input("Senha", type="password", key="password_input")
    if st.button("Entrar"):
        if do_login(user, password):
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha inválidos")
else:
    st.success(f"Logado como {st.session_state.get('user_input','')}")
    
    # Seu conteúdo protegido aqui
    st.title("Dados da planilha")
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    try:
        creds = Credentials.from_service_account_info(
            st.secrets["google_service_account"],
            scopes=SCOPES,
        )
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(st.secrets["SHEET_ID"])
        sheet = spreadsheet.worksheet("dados")
        data = sheet.get_all_records()
        st.dataframe(data)
    except Exception as e:
        st.error(f"Erro ao ler planilha: {e}")

    if st.button("Logout"):
        logout()
        st.experimental_rerun()
