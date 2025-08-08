import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
import time
import gspread
from google.oauth2.service_account import Credentials

# Configurações da sessão (via secrets)
SESSION_TIMEOUT_MINUTES = int(st.secrets.get("SESSION_TIMEOUT_MINUTES", "10"))
COOKIE_PASSWORD = st.secrets.get("COOKIE_PASSWORD", "troque_essa_senha_agora")

# Inicializa cookies
cookies = EncryptedCookieManager(prefix="myapp_", password=COOKIE_PASSWORD)
if not cookies.ready():
    st.stop()  # espera cookies carregarem

def is_logged_in():
    login_info = cookies.get("login_info")
    if not login_info:
        return False
    try:
        login_data = eval(login_info)
        login_time = login_data.get("login_time")
        if login_time is None:
            return False
        # Verifica se sessão expirou
        if time.time() - login_time > SESSION_TIMEOUT_MINUTES * 60:
            # Remove cookie expirado
            if "login_info" in cookies:
                del cookies["login_info"]
                cookies.save()
            return False
        return True
    except Exception:
        return False

def set_login():
    login_data = {"login_time": time.time()}
    cookies["login_info"] = str(login_data)
    cookies.save()

def clear_login():
    if "login_info" in cookies:
        del cookies["login_info"]
        cookies.save()

def login(user, password):
    if user == st.secrets["APP_USER"] and password == st.secrets["APP_PASSWORD"]:
        set_login()
        return True
    return False

def handle_login():
    user = st.session_state.get("user_input", "")
    password = st.session_state.get("password_input", "")
    if login(user, password):
        st.experimental_rerun()
        return  # interrompe execução após rerun
    else:
        st.session_state.login_failed = True

def handle_logout():
    clear_login()
    st.experimental_rerun()
    return

if "login_failed" not in st.session_state:
    st.session_state.login_failed = False

if not is_logged_in():
    st.title("Login do Sistema")
    st.text_input("Usuário", key="user_input")
    st.text_input("Senha", type="password", key="password_input")
    st.button("Entrar", on_click=handle_login)

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

    st.button("Logout", on_click=handle_logout)
