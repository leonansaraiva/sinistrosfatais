import streamlit as st
import time

SESSION_TIMEOUT_MINUTES = 10

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.login_time = 0
    st.session_state.login_failed = False
    st.session_state.login_attempted = False  # controla tentativa recente

def is_logged_in():
    if not st.session_state.logged_in:
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

if not is_logged_in():
    st.title("Login")

    user = st.text_input("Usuário", key="user_input")
    pwd = st.text_input("Senha", type="password", key="password_input")

    if st.button("Entrar"):
        success = try_login(user, pwd)
        st.session_state.login_attempted = True  # marca que tentou logar

    # Esse bloco força a atualizar a interface logo após o login na próxima execução
    if st.session_state.login_attempted:
        st.experimental_rerun = lambda: None  # bloqueia rerun oficial
        if is_logged_in():
            st.experimental_rerun = None
            # nada aqui, só deixa a tela atualizar na próxima execução
        else:
            st.session_state.login_attempted = False

    if st.session_state.login_failed:
        st.error("Usuário ou senha inválidos")

else:
    st.success("Você está logado!")
    st.write("Conteúdo protegido aqui...")

    if st.button("Logout"):
        logout()
