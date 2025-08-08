import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
import time

SESSION_TIMEOUT_MINUTES = int(st.secrets.get("SESSION_TIMEOUT_MINUTES", "10"))
COOKIE_PASSWORD = st.secrets.get("COOKIE_PASSWORD", "troque_essa_senha_agora")

cookies = EncryptedCookieManager(prefix="myapp_", password=COOKIE_PASSWORD)
if not cookies.ready():
    st.stop()

def is_logged_in():
    login_info = cookies.get("login_info")
    if not login_info:
        return False
    try:
        login_data = eval(login_info)
        login_time = login_data.get("login_time")
        if login_time is None:
            return False
        if time.time() - login_time > SESSION_TIMEOUT_MINUTES * 60:
            cookies["login_info"] = None
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
    if login(st.session_state.user_input, st.session_state.password_input):
        st.experimental_rerun()
        return

def handle_logout():
    clear_login()
    st.experimental_rerun()
    return

if not is_logged_in():
    st.title("Login do Sistema")
    st.text_input("Usuário", key="user_input")
    st.text_input("Senha", type="password", key="password_input")
    st.button("Entrar", on_click=handle_login)

    if "login_failed" in st.session_state and st.session_state.login_failed:
        st.error("Usuário ou senha inválidos")
else:
    st.success("Login realizado com sucesso!")
    st.write("Você está logado!")

    # Conteúdo protegido aqui
    if st.button("Logout", on_click=handle_logout):
        pass
