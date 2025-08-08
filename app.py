import streamlit as st
import time

SESSION_TIMEOUT_MINUTES = 10

def is_logged_in():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        return False
    if time.time() - st.session_state.login_time > SESSION_TIMEOUT_MINUTES * 60:
        st.session_state.logged_in = False
        return False
    return True

def try_login(user, pwd):
    if user == st.secrets["APP_USER"] and pwd == st.secrets["APP_PASSWORD"]:
        st.session_state.logged_in = True
        st.session_state.login_time = time.time()
        st.session_state.login_failed = False
        return True
    else:
        st.session_state.logged_in = False
        st.session_state.login_failed = True
        return False

def logout():
    st.session_state.logged_in = False
    st.session_state.login_failed = False
    # clear query params on logout
    st.query_params.clear()
    st.experimental_set_query_params()  # This line removed as per the new API

def force_rerun():
    # Get current query params
    params = st.query_params
    # Toggle a dummy param to force rerun
    dummy = params.get("dummy", ["0"])[0]
    new_value = "1" if dummy == "0" else "0"
    # Update query params to force rerun
    st.query_params = {"dummy": new_value}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.login_time = 0
    st.session_state.login_failed = False

if not is_logged_in():
    st.title("Login")
    user = st.text_input("Usuário", key="user_input")
    pwd = st.text_input("Senha", type="password", key="password_input")
    if st.button("Entrar"):
        success = try_login(user, pwd)
        if success:
            force_rerun()  # Force rerun via query param toggle
    if st.session_state.login_failed:
        st.error("Usuário ou senha inválidos")
else:
    st.success("Você está logado!")
    st.write("Conteúdo protegido aqui...")

    if st.button("Logout"):
        logout()
        force_rerun()
