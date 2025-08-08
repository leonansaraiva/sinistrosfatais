import streamlit as st
import time

SESSION_TIMEOUT_MINUTES = 10

def do_login():
    user = st.session_state.user_input
    pwd = st.session_state.password_input
    if user == st.secrets["APP_USER"] and pwd == st.secrets["APP_PASSWORD"]:
        st.session_state.logged_in = True
        st.session_state.login_time = time.time()
        st.session_state.login_failed = False
        st.experimental_rerun()
        return
    else:
        st.session_state.login_failed = True

def do_logout():
    st.session_state.logged_in = False
    st.experimental_rerun()
    return

def is_logged_in():
    if st.session_state.get("logged_in", False):
        login_time = st.session_state.get("login_time", 0)
        if time.time() - login_time > SESSION_TIMEOUT_MINUTES * 60:
            st.session_state.logged_in = False
            return False
        return True
    return False

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_failed" not in st.session_state:
    st.session_state.login_failed = False

if not is_logged_in():
    st.title("Login")
    st.text_input("Usuário", key="user_input")
    st.text_input("Senha", type="password", key="password_input")
    st.button("Entrar", on_click=do_login)

    if st.session_state.login_failed:
        st.error("Usuário ou senha inválidos")
else:
    st.success("Você está logado!")

    # Conteúdo protegido aqui

    if st.button("Logout", on_click=do_logout):
        pass
