import streamlit as st
import time

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
        st.experimental_rerun()
    else:
        st.session_state.login_failed = True

def logout():
    st.session_state.logged_in = False
    st.session_state.login_failed = False
    st.experimental_rerun()

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

    st.button("Logout", on_click=logout)
