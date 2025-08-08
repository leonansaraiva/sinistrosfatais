import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
import time
import os

# Configurações da sessão via variáveis de ambiente ou st.secrets
SESSION_TIMEOUT_MINUTES = int(st.secrets.get("SESSION_TIMEOUT_MINUTES", "10"))
COOKIE_PASSWORD = st.secrets.get("COOKIE_PASSWORD", "troque_essa_senha_agora")

# Inicializa cookies
cookies = EncryptedCookieManager(prefix="myapp_", password=COOKIE_PASSWORD)

if not cookies.ready():
    st.stop()  # Espera o cookie estar pronto

def is_logged_in():
    """Checa se usuário está logado e se sessão está válida."""
    login_info = cookies.get("login_info")
    if not login_info:
        return False
    # login_info é esperado ser dict salvo como string
    try:
        login_data = eval(login_info)
        login_time = login_data.get("login_time")
        if login_time is None:
            return False
        # Verifica timeout
        if time.time() - login_time > SESSION_TIMEOUT_MINUTES * 60:
            # Sessão expirada
            cookies["login_info"] = None
            cookies.save()
            return False
        return True
    except Exception:
        return False

def set_login():
    """Salva login e timestamp nos cookies."""
    login_data = {"login_time": time.time()}
    cookies["login_info"] = str(login_data)
    cookies.save()

def clear_login():
    cookies["login_info"] = None
    cookies.save()

def login(user, password):
    if user == st.secrets["APP_USER"] and password == st.secrets["APP_PASSWORD"]:
        set_login()
        return True
    return False

if not is_logged_in():
    st.title("Login do Sistema")
    user = st.text_input("Usuário", key="user_input")
    password = st.text_input("Senha", type="password", key="password_input")
    if st.button("Entrar"):
        if login(user, password):
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha inválidos")
else:
    st.success("Login realizado com sucesso!")
    st.write("Você está logado!")

    # Seu conteúdo protegido aqui (ex: planilha google)
    st.title("Teste Google Sheets direto")
    import gspread
    from google.oauth2.service_account import Credentials

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
        clear_login()
        st.experimental_rerun()
