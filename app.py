import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Inicializa variáveis de estado
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_failed" not in st.session_state:
    st.session_state.login_failed = False

def login():
    user = st.session_state.get("user_input", "")
    password = st.session_state.get("password_input", "")
    if user == st.secrets["APP_USER"] and password == st.secrets["APP_PASSWORD"]:
        st.session_state.logged_in = True
        st.session_state.login_failed = False
    else:
        st.session_state.logged_in = False
        st.session_state.login_failed = True

if not st.session_state.logged_in:
    st.title("Login do Sistema")
    st.text_input("Usuário", key="user_input")
    st.text_input("Senha", type="password", key="password_input")
    st.button("Entrar", on_click=login)

    if st.session_state.login_failed:
        st.error("Usuário ou senha inválidos")
else:
    st.success("Login realizado com sucesso!")
    st.write("Você está logado!")

    st.title("Teste Google Sheets direto")

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

    # Botão de logout para facilitar teste
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()
